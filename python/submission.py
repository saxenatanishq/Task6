"""
Homework 5
Submission Functions
"""

# import packages here
import numpy as np

"""
Q3.1.1 Eight Point Algorithm
       [I] pts1, points in image 1 (Nx2 matrix)
           pts2, points in image 2 (Nx2 matrix)
           M, scalar value computed as max(H1,W1)
       [O] F, the fundamental matrix (3x3 matrix)
"""

def normalize_points(points,M):
    centroid = np.mean(points, axis=0)
    shifted_points = points - centroid
    normalized_points = shifted_points/M
    
    # Construct transformation matrix T
    T = np.array([
        [1/M,   0,   -centroid[0] / M],
        [0,   1/M,   -centroid[1] / M],
        [0,     0,    1]
    ])
    
    return normalized_points, T


def eight_point(pts1, pts2, M):
    # Normalize the points
    pts1, T1 = normalize_points(pts1, M)
    pts2, T2 = normalize_points(pts2, M)

    n = pts1.shape[0]
    A = np.zeros((n, 9)) # In our case n is 110
    
    for i in range(n):
        x1, y1 = pts1[i]
        x2, y2 = pts2[i]
        A[i] = [x1*x2, x1*y2, x1, y1*x2, y1*y2, y1, x2, y2, 1]
    
    # Compute F using SVD
    U, S, Vt = np.linalg.svd(A)
    F = Vt[-1].reshape(3, 3)
    
    # Enforce rank-2 constraint
    U, S, Vt = np.linalg.svd(F)
    S[-1] = 0
    F = U @ np.diag(S) @ Vt
    
    # Unnormalize F
    F = T2.T @ F @ T1
    
    return F

"""
Q3.1.2 Epipolar Correspondences
       [I] im1, image 1 (H1xW1 matrix)
           im2, image 2 (H2xW2 matrix)
           F, fundamental matrix from image 1 to image 2 (3x3 matrix)
           pts1, points in image 1 (Nx2 matrix)
       [O] pts2, points in image 2 (Nx2 matrix)
"""

def epipolar_correspondences(im1, im2, F, pts1, window_size=5, Range = 20):
    h, w = im2.shape[:2]
    pts2 = np.zeros_like(pts1)
    
    for i, (x1, y1) in enumerate(pts1):
        # Compute the epipolar line in image 2 using teh point in image 1
        line = F @ np.array([x1, y1, 1])
        a, b, c = line # Coefficient of the line (a is the coeff of x, b --> y and c is constant)
        
        # Search along the epipolar line
        best_x2, best_y2 = 0, 0
        min_error = float('inf')
        
        for x2 in range(max(0, int(x1 - Range)), min(w, int(x1 + Range))):
            y2 = int((-a*x2-c)/b) if b!=0 else int(y1)
            
            if 0<=y2<h:
                patch1 = im1[int(y1 - window_size):int(y1 + window_size + 1),int(x1 - window_size):int(x1 + window_size + 1)]
                patch2 = im2[int(y2 - window_size):int(y2 + window_size + 1),int(x2 - window_size):int(x2 + window_size + 1)]
                
                if patch1.shape == patch2.shape:
                    error = np.sum((patch1.astype(np.float32) - patch2.astype(np.float32))**2)
                    if error < min_error:
                        min_error = error
                        best_x2, best_y2 = x2, y2
        
        pts2[i] = [best_x2, best_y2]
    
    return pts2

"""
Q3.1.3 Essential Matrix
       [I] F, the fundamental matrix (3x3 matrix)
           K1, camera matrix 1 (3x3 matrix)
           K2, camera matrix 2 (3x3 matrix)
       [O] E, the essential matrix (3x3 matrix)
"""


def essential_matrix(F, K1, K2):
    
    E = K2.T @ F @ K1  # Compute E using the relation E=K2^T*F*K1
    return E


"""
Q3.1.4 Triangulation
       [I] P1, camera projection matrix 1 (3x4 matrix)
           pts1, points in image 1 (Nx2 matrix)
           P2, camera projection matrix 2 (3x4 matrix)
           pts2, points in image 2 (Nx2 matrix)
       [O] pts3d, 3D points in space (Nx3 matrix)
"""

def triangulate(P1, pts1, P2, pts2):
    pass
    

"""
Q3.2.1 Image Rectification
       [I] K1 K2, camera matrices (3x3 matrix)
           R1 R2, rotation matrices (3x3 matrix)
           t1 t2, translation vectors (3x1 matrix)
       [O] M1 M2, rectification matrices (3x3 matrix)
           K1p K2p, rectified camera matrices (3x3 matrix)
           R1p R2p, rectified rotation matrices (3x3 matrix)
           t1p t2p, rectified translation vectors (3x1 matrix)
"""
def rectify_pair(K1, K2, R1, R2, t1, t2):
    # replace pass by your implementation
    pass

"""
Q3.2.2 Disparity Map
       [I] im1, image 1 (H1xW1 matrix)
           im2, image 2 (H2xW2 matrix)
           max_disp, scalar maximum disparity value
           win_size, scalar window size value
       [O] dispM, disparity map (H1xW1 matrix)
"""
def get_disparity(im1, im2, max_disp, win_size):
    # replace pass by your implementation
    pass

"""
Q3.2.3 Depth Map
       [I] dispM, disparity map (H1xW1 matrix)
           K1 K2, camera matrices (3x3 matrix)
           R1 R2, rotation matrices (3x3 matrix)
           t1 t2, translation vectors (3x1 matrix)
       [O] depthM, depth map (H1xW1 matrix)
"""
def get_depth(dispM, K1, K2, R1, R2, t1, t2):
    # replace pass by your implementation
    pass

"""
Q3.3.1 Camera Matrix Estimation
       [I] x, 2D points (Nx2 matrix)
           X, 3D points (Nx3 matrix)
       [O] P, camera matrix (3x4 matrix)
"""
def estimate_pose(x, X):
    # replace pass by your implementation
    pass

"""
Q3.3.2 Camera Parameter Estimation
       [I] P, camera matrix (3x4 matrix)
       [O] K, camera intrinsics (3x3 matrix)
           R, camera extrinsics rotation (3x3 matrix)
           t, camera extrinsics translation (3x1 matrix)
"""
def estimate_params(P):
    # replace pass by your implementation
    pass
