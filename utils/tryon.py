import cv2
import mediapipe as mp
import numpy as np
import os
import random

def get_random_accessory(accessory_type):
    """Get a random accessory image from the specified type directory"""
    accessory_dir = os.path.join('static/accessories', accessory_type)
    if not os.path.exists(accessory_dir):
        return None
    
    files = [f for f in os.listdir(accessory_dir) if f.endswith(('.png', '.jpg', '.jpeg'))]
    if not files:
        return None
    
    return os.path.join(accessory_dir, random.choice(files))

def calculate_sunglasses_transform(landmarks, image_shape, glasses_shape):
    """Calculate the transformation parameters for sunglasses"""
    h, w = image_shape[:2]
    gh, gw = glasses_shape[:2]
    
    # Get eye landmarks - using more accurate eye corner points
    left_eye_outer = np.array([landmarks[33].x * w, landmarks[33].y * h])
    left_eye_inner = np.array([landmarks[133].x * w, landmarks[133].y * h])
    right_eye_inner = np.array([landmarks[362].x * w, landmarks[362].y * h])
    right_eye_outer = np.array([landmarks[263].x * w, landmarks[263].y * h])
    
    # Get additional facial landmarks
    nose_bridge = np.array([landmarks[168].x * w, landmarks[168].y * h])
    nose_tip = np.array([landmarks[1].x * w, landmarks[1].y * h])
    
    # Calculate eye centers
    left_eye = (left_eye_outer + left_eye_inner) / 2
    right_eye = (right_eye_outer + right_eye_inner) / 2
    
    # Calculate angle
    eye_angle = np.degrees(np.arctan2(right_eye[1] - left_eye[1],
                                     right_eye[0] - left_eye[0]))
    
    # Calculate scale with increased size
    eye_distance = np.linalg.norm(right_eye - left_eye)
    face_width = np.linalg.norm(right_eye_outer - left_eye_outer)
    
    # Increased scaling factors for larger glasses
    scale_eye = eye_distance / (gw * 0.35)    # Reduced from 0.45 to make larger
    scale_face = face_width / (gw * 0.75)     # Reduced from 0.95 to make larger
    scale = (scale_eye * 0.4 + scale_face * 0.6) * 1.2  # Weighted average with 20% size increase
    
    # Calculate center position
    center_x = (left_eye[0] + right_eye[0]) / 2
    
    # Calculate vertical position with multiple reference points
    eye_level = (left_eye[1] + right_eye[1]) / 2
    ideal_glasses_pos = nose_bridge[1] + (eye_level - nose_bridge[1]) * 0.15  # Adjusted position
    
    # Weighted positioning using nose bridge and eye level
    center_y = 0.65 * ideal_glasses_pos + 0.35 * eye_level
    
    return center_x, center_y, scale, eye_angle

def calculate_hat_transform(landmarks, image_shape, hat_shape):
    """Calculate the transformation parameters for hats"""
    h, w = image_shape[:2]
    hat_h, hat_w = hat_shape[:2]
    
    # Get head landmarks
    forehead_top = np.array([landmarks[10].x * w, landmarks[10].y * h])  # Top of forehead
    forehead_mid = np.array([landmarks[151].x * w, landmarks[151].y * h])  # Mid forehead
    left_temple = np.array([landmarks[447].x * w, landmarks[447].y * h])  # Left temple
    right_temple = np.array([landmarks[227].x * w, landmarks[227].y * h])  # Right temple
    
    # Get additional landmarks for better head measurement
    left_ear_top = np.array([landmarks[162].x * w, landmarks[162].y * h])  # Left ear top
    right_ear_top = np.array([landmarks[389].x * w, landmarks[389].y * h])  # Right ear top
    
    # Calculate head width using ear positions for better proportion
    head_width = np.linalg.norm(right_ear_top - left_ear_top) * 1.25  # Slightly reduced width multiplier
    
    # Center position using ear tops for better horizontal placement
    center_x = (left_ear_top[0] + right_ear_top[0]) / 2
    
    # Calculate scale based on head width and hat dimensions
    # Adjust scale to make hat fit properly on head
    scale = head_width / (hat_w * 0.81)  # Increased divisor to make hat slightly smaller
    
    # Calculate angle based on ear positions for better alignment
    dx = right_ear_top[0] - left_ear_top[0]
    dy = right_ear_top[1] - left_ear_top[1]
    angle = np.degrees(np.arctan2(dy, dx)) + 360
    
    # Position hat on head with adjusted vertical placement
    # Calculate vertical position relative to forehead
    forehead_height = forehead_top[1] - forehead_mid[1]
    
    # Adjust vertical position to overlap with forehead
    vertical_offset = hat_h * scale * 0.17  # Further reduced offset to lower the hat more
    # Move hat down to overlap with forehead
    center_y = forehead_mid[1] - vertical_offset + (forehead_height * 0.8)  # Increased forehead factor for better overlap
    
    return center_x, center_y, scale, angle

def virtual_tryon(image_path, accessory_type):
    # Read the input image
    image = cv2.imread(image_path)
    if image is None:
        return image_path
    
    h, w = image.shape[:2]

    # Initialize MediaPipe Face Mesh
    mp_face = mp.solutions.face_mesh
    face_mesh = mp_face.FaceMesh(static_image_mode=True, max_num_faces=1,
                                min_detection_confidence=0.5, min_tracking_confidence=0.5)

    # Process the image
    results = face_mesh.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

    if not results.multi_face_landmarks:
        return image_path

    landmarks = results.multi_face_landmarks[0].landmark

    # Get the specific accessory based on type
    if accessory_type.startswith('sunglasses'):
        accessory_path = f'static/accessories/sunglasses/{accessory_type}.png'
    elif accessory_type.startswith('hat'):
        accessory_path = f'static/accessories/hats/{accessory_type}.png'
    else:
        accessory_path = f'static/accessories/{accessory_type}/{accessory_type}.png'

    if not os.path.exists(accessory_path):
        return image_path

    # Read the accessory image with alpha channel
    accessory_img = cv2.imread(accessory_path, cv2.IMREAD_UNCHANGED)
    if accessory_img is None:
        return image_path

    if accessory_type.startswith('sunglasses'):
        # Get transformation parameters for sunglasses
        center_x, center_y, scale, angle = calculate_sunglasses_transform(
            landmarks, image.shape, accessory_img.shape)
    elif accessory_type.startswith('hat'):
        # Get transformation parameters for hats
        center_x, center_y, scale, angle = calculate_hat_transform(
            landmarks, image.shape, accessory_img.shape)
    
    # Create transformation matrix
    M = cv2.getRotationMatrix2D((accessory_img.shape[1]/2, accessory_img.shape[0]/2), angle, scale)
    M[:, 2] += [center_x - accessory_img.shape[1]/2, center_y - accessory_img.shape[0]/2]
    
    # Warp the accessory image
    warped_accessory = cv2.warpAffine(accessory_img, M, (w, h), 
                                     flags=cv2.INTER_LINEAR, 
                                     borderMode=cv2.BORDER_TRANSPARENT)
    
    # Create mask from alpha channel
    if warped_accessory.shape[2] == 4:
        alpha = warped_accessory[:, :, 3] / 255.0
        alpha = np.stack([alpha] * 3, axis=-1)
        
        # Blend images
        warped_rgb = warped_accessory[:, :, :3]
        image = (warped_rgb * alpha + image * (1 - alpha)).astype(np.uint8)

    # Save the result
    output_path = os.path.join("static/uploads", f"output_{os.path.basename(image_path)}")
    cv2.imwrite(output_path, image)
    return output_path
