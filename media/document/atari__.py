import numpy as np
import PIL
import torch
import torch.nn as nn
import onnx
import gym
import time

import string

all_letters = string.ascii_letters + " .,;'"
n_letters = len(all_letters)

def letterToIndex(letter):
    return all_letters.find(letter)

# Just for demonstration, turn a letter into a <1 x n_letters> Tensor
def letterToTensor(letter):
    tensor = torch.zeros(1, n_letters)
    tensor[0][letterToIndex(letter)] = 1
    return tensor

# Turn a line into a <line_length x 1 x n_letters>,
# or an array of one-hot letter vectors
def lineToTensor(line):
    tensor = torch.zeros(len(line), 1, n_letters)
    for li, letter in enumerate(line):
        tensor[li][0][letterToIndex(letter)] = 1
    return tensor

class RNN(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(RNN, self).__init__()

        self.hidden_size = hidden_size

        self.i2h = nn.Linear(input_size + hidden_size, hidden_size)
        self.i2o = nn.Linear(input_size + hidden_size, output_size)
        self.softmax = nn.LogSoftmax(dim=1)

    def forward(self, input, hidden):
        if torch.cuda.is_available():
          input, hidden = input.cuda(), hidden.cuda()
        combined = torch.cat((input, hidden), 1)
        hidden = nn.LeakyReLU()(self.i2h(combined))
        output = nn.LeakyReLU()(self.i2o(combined))
        output = self.softmax(output)
        return output, hidden

    def initHidden(self):
        return torch.zeros(1, self.hidden_size)

loaded = torch.load("rnn_100000.pt",map_location=torch.device('cpu'))

torch.save({
	"state_dict":loaded["model_state_dict"]
	},"rnn_url.pt")

# print(lineToTensor("https://hello.com").shape)

# rnn = RNN(n_letters,20,3)
# rnn.load_state_dict(loaded["model_state_dict"])
# rnn.eval()

# all_categories = ['url','link','normal']

# def predict(line):
#     lineTensor = lineToTensor(line)
#     hidden = rnn.initHidden()
#     for i in range(lineTensor.size()[0]):
#         output,hidden = rnn(lineTensor[i],hidden)

#     return all_categories[output.max(-1)[-1][0]]

# line = "gxqhtawh.org/information.cgi"
# print(predict(line))

#
# MIN_EXP = 50000
# MAX_EXP = 500000
# TARGET_UPDATE_PER = 10000
# IM_SIZE = 84
# K = 4
#
#
# def ImageTransform(image):
#     image = torchvision.transforms.ToPILImage()(image)
#     image = torchvision.transforms.functional.to_grayscale(image)
#     image = torchvision.transforms.functional.resized_crop(image, 34, 0, 160, 160, (IM_SIZE, IM_SIZE))
#     image = torchvision.transforms.functional.to_tensor(image)
#     return image.squeeze()
#
#
# def update_state(state, obs_small):
#     return np.append(state[:, :, 1:], np.expand_dims(obs_small, 2), axis=2)
#
#
# class ReplayMemory:
#
#     def __init__(self, size=MAX_EXP, frame_h=IM_SIZE, frame_w=IM_SIZE, agent_history_length=4,
#                  batch_size=32):
#         self.size = size
#         self.frame_h = frame_h
#         self.frame_w = frame_w
#         self.agen_history_length = agent_history_length
#         self.batch_size = batch_size
#         self.count = 0
#         self.current = 0
#
#         self.actions = np.empty(size, dtype=np.int32)
#         self.rewards = np.empty(self.size, dtype=np.float32)
#         self.frames = np.empty((self.size, self.frame_h, self.frame_w), dtype=np.float32)
#         self.terminal_flags = np.empty(self.size, dtype=np.bool)
#
#         self.states = np.empty((self.batch_size, self.agen_history_length, self.frame_h, self.frame_w)
#                                , dtype=np.float32)
#         self.new_states = np.empty((self.batch_size, self.agen_history_length,
#                                     self.frame_h, self.frame_w), dtype=np.float32)
#         self.indices = np.empty(self.batch_size, dtype=np.int32)
#
#     def add_experience(self, action, frame, reward, terminal):
#
#         if frame.shape != (self.frame_h, self.frame_w):
#             raise ValueError("DIMENSION INCORRECT")
#
#         self.actions[self.current] = action
#         self.frames[self.current, ...] = frame
#         self.rewards[self.current] = reward
#         self.terminal_flags[self.current] = reward
#         self.count = max(self.count, self.current + 1)
#         self.current = (self.current + 1) % self.size
#
#     def _get_state(self, index):
#         if self.count is 0:
#             raise ValueError("THE REPLAY MEMORY")
#         if index < self.agen_history_length - 1:
#             raise ValueError("INDEX MUST BE MIN 3")
#         return self.frames[index - self.agen_history_length + 1:index + 1, ...]
#
#     def _get_valid_indices(self):
#         for i in range(self.batch_size):
#             while True:
#                 index = np.random.randint(self.agen_history_length, self.count - 1)
#                 if index < self.agen_history_length:
#                     print("ok")
#                     continue
#                 if index >= self.current and index - self.agen_history_length <= self.current:
#                     continue
#                 if self.terminal_flags[index - self.agen_history_length:index].any():
#                     continue
#                 break
#             self.indices[i] = index
#
#     def get_minibatch(self):
#
#         if self.count < self.agen_history_length:
#             raise ValueError('NOT ENOUGH MEMORIES')
#
#         self._get_valid_indices()
#         for i, idx in enumerate(self.indices):
#             self.states[i] = self._get_state(idx - 1)
#             self.new_states[i] = self._get_state(idx)
#         return np.transpose(self.states, axes=(0, 2, 3, 1)), self.actions[self.indices], self.rewards[
#             self.indices], np.transpose(self.new_states, axes=(0, 2, 3, 1)), self.terminal_flags[self.indices]
#
#
# state_size = (IM_SIZE,IM_SIZE,4)
#
# gamma = 0.99
# total_episodes = 3500
# class Flatten(nn.Module):
#     def forward(self, x):
#         x = x.view(x.size()[0], -1)
#         return x
#
# class Loss(nn.Module):
#     def forward(self,y_true,y_pred):
#       delta = 1
#       abs_error = torch.abs(y_true-y_pred)
#       loss = torch.where(abs_error<=delta,0.5*abs_error.pow(2),delta*abs_error-(0.5*delta**2))
#       return loss
#
#
# class DQN:
#   def __init__(self,state_size,action_size,lr):
#     self.state_size = state_size
#     self.action_size = action_size
#     self.lr = lr
#
#     self.model = []
#
#     self.model.append(nn.Conv2d(4,32,8,4))
#     self.model.extend([nn.BatchNorm2d(32),nn.ReLU(inplace=True)])
#     self.model.append(nn.Conv2d(32,64,4,2))
#     self.model.extend([nn.BatchNorm2d(64),nn.ReLU(inplace=True)])
#     self.model.append(nn.Conv2d(64,64,3,1))
#     self.model.extend([nn.BatchNorm2d(64),nn.ReLU(inplace=True)])
#
#     self.model.append(Flatten())
#
#     self.model.append(nn.Linear(3136,512))
#     self.model.append(nn.ReLU())
#     self.model.append(nn.Linear(512,self.action_size))
#
#
#     self.model = nn.Sequential(*self.model)
#     if torch.cuda.is_available():
#       self.model = self.model.cuda()
#
#     self.opt = torch.optim.Adam(self.model.parameters(),lr = self.lr)
#     self.loss = Loss()
#
#   def copy(self,model):
#     self.model.load_state_dict(model.model.state_dict())
#   def predict(self,state):
#     state = np.asarray(state)
#     if len(state.shape) ==3:
#       state = torch.from_numpy(state).unsqueeze(0).permute(0,3,1,2).float()
#     else:
#       state = torch.from_numpy(state).permute(0,3,1,2).float()
#     if torch.cuda.is_available():
#       state = state.cuda()
#     return self.model(state)
#
#   def sample_action(self,state,eps):
#     if np.random.random() < eps:
#       return np.random.randint(0,self.action_size)
#     else:
#       actions = self.predict(state)
#       action = np.argmax(actions.cpu().detach())
#       return action
#
#   def update(self,state,action,targets):
#     predicted = self.predict(state)
#
#     # predicted = (predicted*make_one_hot(torch.tensor(action).long(),self.action_size)).sum(1)
#     predicted = predicted[torch.arange(predicted.size(0)),action]
#
#     loss = self.loss(targets.cuda().float(),predicted).mean()
#
#     self.opt.zero_grad()
#     loss.backward()
#     self.opt.step()
#     return loss
# def make_one_hot(labels, C=2):
#     one_hot = torch.cuda.FloatTensor(labels.size(0),C).zero_()
#     one_hot[torch.arange(labels.size(0)),labels] = 1
#
#     return one_hot
#
#
# model__ = torch.load("model1562.pt", map_location=torch.device('cpu') )
# model = model__["model"]
# model.model.load_state_dict(model__["state_dict"])
#
# print(model.model)
# env = gym.make("Breakout-v0")
# obs = env.reset()
# obs_small = ImageTransform(obs).numpy()
# state = np.stack([obs_small]*4,axis = 2)
# done = False
# rews=0
# re = 0
# while not done and rews<2000:
#     env.render()
#
#     action = model.sample_action(state,0.01)
#
#     time.sleep(0.01)
#
#     obs,rew,done,info = env.step(action)
#     rews+=1
#     re+=rew
#     obs_small = ImageTransform(obs).numpy()
#     next_state = update_state(state,obs_small)
#
#
#     state = next_state
#
# print(rews,re)
