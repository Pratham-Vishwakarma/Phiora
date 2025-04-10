import cv2
import mediapipe as mp
import numpy as np

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=True)

face_shape_hairstyles = {
    "Triangle": "Blunt or side-swept bangs to cover a broad forehead. Face-framing layers to soften a pointy chin. Glossy, blow-dried waves or beachy waves add volume and balance. Short, wavy bobs or sleek bobs like the 'Posh Bob.' High buns with tendrils or braided buns for elegance. Long sleek pixies or textured pixies for a chic look.",
    "Heart": "Long, piecey bangs or curtain bangs to soften the forehead. Long layered lobs or medium cuts with side-swept bangs to balance the jawline. Beachy waves or loose waves to add softness. Shaggy pixies or pixies with bangs to highlight cheekbones. Wavy lobs styled with a middle or side part for elegance.",
    "Oblong": "Full, blunt bangs to visually shorten the face length. Medium-length cuts with layers to add width and volume. Loose curls or waves to create softness. Chin-length bobs add width and balance to the face.",
    "Diamond": "Side-swept bangs to soften angular features. Cuts with medium layers that add width at the chin level. Beach waves or soft curls to balance narrow features. Textured pixies that emphasize cheekbones.",
    "Oval": "Most styles suit this shape. Long layers, sleek bobs, and pixie cuts all work well. Beachy waves or loose curls add texture. Curtain bangs or side-swept bangs provide a modern touch.",
    "Square": "Long soft layers to soften angular jawlines. Deep side parts to create asymmetry and balance. Loose curls or tousled waves for a softer appearance. Layered bobs that end below the jawline are flattering.",
    "Round": "Long layers to elongate the face and add structure. Side-swept bangs create the illusion of length and angles. Waves and volume at the crown add height and balance. Pixie cuts with volume on top visually elongate the face."
}

def euclidean(p1, p2):
    return np.linalg.norm(np.array(p1) - np.array(p2))

def analyze_face_shape_from_landmarks(landmarks, image_shape):
    height, width = image_shape
    def get_point(idx):
        return int(landmarks[idx].x * width), int(landmarks[idx].y * height)

    jaw_left = get_point(58)
    jaw_right = get_point(288)
    jaw_width = euclidean(jaw_left, jaw_right)

    forehead_left = get_point(21)
    forehead_right = get_point(251)
    forehead_width = euclidean(forehead_left, forehead_right)

    cheek_left = get_point(234)
    cheek_right = get_point(454)
    cheek_width = euclidean(cheek_left, cheek_right)

    chin = get_point(175)
    forehead_top = get_point(10)
    face_length = euclidean(chin, forehead_top)

    width_ratio = forehead_width / jaw_width
    length_ratio = face_length / cheek_width

    abc_length = abs(forehead_width - cheek_width) / cheek_width
    def_length = abs(jaw_width - cheek_width) / cheek_width

    if (
        jaw_width > forehead_width and
        length_ratio > 1.1 and
        jaw_width > cheek_width * 0.95
    ):
        return "Triangle"

    if (
        width_ratio > 1.05 and
        forehead_width > cheek_width > jaw_width and
        length_ratio >= 1.1 and
        abc_length < 0.07 and
        def_length > 0.09
    ):
        return "Heart"

    elif length_ratio >= 1.2 and abc_length < 0.15 and def_length < 0.15:
        return "Oblong"

    elif (
        cheek_width > forehead_width and
        cheek_width > jaw_width and
        1.13 <= length_ratio <= 1.25 and
        abc_length < 0.05 and
        0.15 >= def_length >= 0.11
    ):
        return "Diamond"

    elif (
        1.12 < length_ratio <= 1.3 and
        abc_length < 0.08 and
        forehead_width > jaw_width and
        def_length > 0.08
    ):
        return "Oval"

    elif (
        abs(width_ratio - 1) < 0.13 and
        length_ratio <= 1.15 and
        abc_length < 0.061 and
        def_length < 0.13
    ):
        return "Square"

    elif face_length < cheek_width * 1.1:
        return "Round"

    return "Unknown"

def face_shape(image_path):
    image = cv2.imread(image_path)
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb)

    if results.multi_face_landmarks:
        face_landmarks = results.multi_face_landmarks[0]
        shape = analyze_face_shape_from_landmarks(face_landmarks.landmark, image.shape[:2])        

        if shape in face_shape_hairstyles:
            return shape, face_shape_hairstyles[shape]
        else:
            return "Unknown", "No specific hairstyle recommendation available."
            
    else:
        return "No face detected", "No specific hairstyle recommendation available."
