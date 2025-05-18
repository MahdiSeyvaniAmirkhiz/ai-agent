import cv2
import numpy as np


def apply_color_shift(frame, amplitude, intensity=1.0):
    """Shift colors based on amplitude."""
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV).astype(np.float32)
    hsv[..., 0] = (hsv[..., 0] + amplitude * 180 * intensity) % 180
    hsv[..., 1] = np.clip(hsv[..., 1] + amplitude * 50 * intensity, 0, 255)
    result = cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2BGR)
    return result


def apply_blur(frame, amplitude, intensity=1.0):
    k = int(1 + amplitude * 10 * intensity)
    if k % 2 == 0:
        k += 1
    blurred = cv2.GaussianBlur(frame, (k, k), 0)
    return blurred
