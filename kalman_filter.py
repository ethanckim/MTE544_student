import numpy as np

# Part 3: Comment the code explaining each part
class kalman_filter:
    
    # Part 3: Initialize the covariances and the states
    def __init__(self, P,Q,R, x, dt):
        # Just initialize to values that are passed in
        self.P = P
        self.Q = Q
        self.R = R
        self.x = x
        self.dt = dt
        
    # Part 3: Replace the matrices with Jacobians where needed
    def predict(self):

        # Update the state transition and measurement matrices with corresponding Jacobians
        # Note variables are renamed to match lecture notation
        self.G = self.jacobian_G()
        self.H = self.jacobian_H()

        # Predict the new state and covariance
        self.motion_model()
        self.P= np.dot(np.dot(self.G, self.P), self.G.T) + self.Q

    # Part 3: Replace the matrices with Jacobians where needed
    def update(self, z):
        # This was already implemented but we confirmed it matches the algorithm correctly

        # Compute the kalman gain - dont need to update with jacobians because predict() will do that
        S= np.dot(np.dot(self.H, self.P), self.H.T) + self.R
        kalman_gain=np.dot(np.dot(self.P, self.H.T), np.linalg.inv(S))

        # Computing Innovation
        surprise_error= z - self.measurement_model()

        # Update the state and covariance
        self.x=self.x + np.dot(kalman_gain, surprise_error)
        self.P=np.dot((np.eye(self.G.shape[0]) - np.dot(kalman_gain, self.H)), self.P)
        
    
    # Part 3: Implement here the measurement model
    def measurement_model(self):
        x, y, th, w, v, vdot = self.x

        # Return expected measurements
        return np.array([
            v, # v
            w, # w
            vdot, # ax
            v * w, # ay definition from tutorial
        ])
        
    # Part 3: Implement the motion model (state-transition matrice)
    def motion_model(self):
        
        x, y, th, w, v, vdot = self.x
        dt = self.dt

        # Predict the new state using the motion model for 2WD
        self.x = np.array([
            x + v * np.cos(th) * dt, # split v into x component
            y + v * np.sin(th) * dt, # split v into y component
            th + w * dt,
            w,
            v  + vdot*dt,
            vdot,
        ])

    
    def jacobian_G(self):
        x, y, th, w, v, vdot = self.x
        dt = self.dt

        # Compute the Jacobian of the motion model - predicted state vs previous state
        return np.array([
            #x, y,               th, w,             v, vdot
            [1, 0,              -v * np.sin(th) * dt, 0,          np.cos(th) * dt,  0],
            [0, 1,              v * np.cos(th) * dt, 0,          np.sin(th) * dt,  0],
            [0, 0,                1, dt,           0,  0],
            [0, 0,                0, 1,            0,  0],
            [0, 0,                0, 0,            1,  dt],
            [0, 0,                0, 0,            0,  1 ]
        ])
    
    
    # Part 3: Implement here the jacobian of the H matrix (measurements)
    def jacobian_H(self):
        x, y, th, w, v, vdot=self.x

        # Compute the Jacobian of the measurement model
        return np.array([
            #x, y,th, w, v,vdot
            [0,0,0  , 0, 1, 0], # v
            [0,0,0  , 1, 0, 0], # w
            [0,0,0  , 0, 0, 1], # ax
            [0,0,0  , v, w, 0], # ay
        ])
        
    # Part 3: return the states here
    def get_states(self):
        return self.x
