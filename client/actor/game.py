from client.actor import trialState
from client.actor import search
#from actor import trialState
#from actor import search



#from scipy import spatial

class Game:
    def __init__(self, frame):
        self.frame = frame
        self.trial = None
        self.search = None
        self.path = None
        self.tar_nodes = None

        self.obstacles = None
        self.targets = None
        self.ball_pos = None
        #self.field_filled = None
        #self.ball_pos = None

    def start(self, frame):
        return None

    def stop(self, frame):
        return None

    #returns the number of trials included in one game
    def experiment_def(self, frame):
        nr_of_trials = frame["Nr_of_Trials"]
        return nr_of_trials

    #initialises the trial state, one game hast several trials.
    #each trial is 1m long and consists of 60fps
    def trial_def(self, frame):
        level_data = frame['Level Data']
        target_data = level_data['Targets']
        ball_data = level_data['Ball']
        obstacle_data = level_data['Obstacles']


        tar_z = target_data['Z']
        tar_y = target_data['Y']
        tar_x = target_data['X']
        tar_radius = target_data['Radius']
        tar_z_size = target_data['Z_size']
        nr_of_targets = level_data['Nr of Targets']

        obs_x = obstacle_data['X']
        obs_y = obstacle_data['Y']
        obs_z = obstacle_data['Z']
        obs_x_size = obstacle_data['X_size']
        obs_y_size = obstacle_data['Y_size']
        obs_z_size = obstacle_data['Z_size']
        obs_z_angle_deg = obstacle_data['Z_angle_deg']
        obs_slowdown_fac = obstacle_data['slowdown factor']
        obs_visibility = obstacle_data['visibility']
        obs_geometric_type = obstacle_data['geometric type']
        nr_of_obstacles = level_data['Nr of Obstacles']

        ball_x = ball_data['X']
        ball_y = ball_data['Y']
        ball_z = ball_data['Z']
        ball_radius = ball_data['Radius']

        ai_type = level_data['AI Type']
        show_bar = level_data['ShowBar']
        nr_of_frames_to_skip_at_start = level_data['Nr_of_Frames_to_Skip_at_Start_of_Trial']
        blink_wave_length_owg = level_data['Blink_Wavelength_OWG']
        blink_wave_length_screen = level_data['Blink_Wavelength_Screen'] #?
        trial_duration_time = level_data['Trial Duration [ms]'] #60000 ms
        aI_length_of_memory = level_data['AI 1 Length of Memory']
        screen_flicker_target_radius = level_data['Screen_Flicker_Target_Radius']
        questionaire_text = level_data['Questionair Text']
        show_fixiation_cross = level_data['Screen_Flicker_Target_Radius']
        trial_type = level_data['Trial Type']

        self.trial = trialState.TrialState(obs_x, obs_y, obs_z, obs_x_size, obs_y_size, obs_z_size, obs_z_angle_deg,
                                           obs_slowdown_fac, obs_visibility, obs_geometric_type, tar_x, tar_y, tar_z,
                                           tar_z_size, tar_radius, ball_x, ball_y, ball_z, ball_radius, nr_of_targets,
                                           nr_of_obstacles)

        #initialises the field with given obstacles and targets
        self.search = search.Search(self.trial.field_filled , self.trial.targets_tup)

        #self.tar_nodes = self.trial.tar_nodes
        self.ball_pos = self.trial.ball
        self.obstacles = self.trial.obstacles
        self.targets = self.trial.targets

        #path to target returned by search
        self.path = self.search.go_for_target(self.trial.ball,(0, 0), self.trial.ball_radius)

    #data about both players submitted in every frame during play
    def play(self, frame):
        frame_data = frame["Frame Data"]

        p1_norm_avg_x = frame_data["Player 1"]['norm_avg_x']
        p1_norm_avg_reshaped_y = frame_data["Player 1"]['norm avg_reshaped y']
        p1_x = frame_data["Player 1"]['X']
        p1_f_x = frame_data["Player 1"]['F_x']
        p1_y = frame_data["Player 1"]['Y']
        p1_f_y = frame_data["Player 1"]['F_y']

        p2_norm_avg_x = frame_data["Player 2"]['norm_avg_x']
        p2_norm_avg_reshaped_y = frame_data["Player 2"]['norm avg_reshaped y']
        p2_x = frame_data["Player 2"]['X']
        p2_f_x = frame_data["Player 2"]['F_y']
        p2_y = frame_data["Player 2"]['Y']

        trigger_state = frame_data['Trigger State']
        start_last_frame = frame_data ['Last Frame Start [ms]']
        trial_start = frame_data['Trial Start [ms]']
        trial_elapsed = frame_data['Trial Elapsed [ms]']
        ode_processed_until = frame_data['ODE processed until [ms]']
        dt = frame_data['dt [ms]']

        x, y = self.search.go_for_target((p1_x, p1_y), (p1_f_x, p1_f_y),self.trial.ball_radius)

        response = {"MsgType": "Receive Frame", "Frame Data": {"X": x, "Y": y}}

        return response
