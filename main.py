import gym
import dqn
import numpy as np
import matplotlib.pyplot as plt
import pickle

ENV_NAME = 'CartPole-v0'
N_TEST = 100
GOAL = 195
MAX_EPISODES = 400


# ENV_NAME = 'CartPole-v1'
# N_TEST = 100
# GOAL = 475
# MAX_EPISODES = 500

# ENV_NAME = 'MountainCar-v0'
# N_TEST = 100
# GOAL = -110
# MAX_EPISODES = 1000

# ENV_NAME = 'Acrobot-v1'
# N_TEST = 100
# GOAL = -100
# MAX_EPISODES = 1000


def play(env, action_select, perceive, render=False):
    ret = 0
    observation = env.reset()
    while True:
        if render: env.render()
        action = action_select(observation)
        nxt_observation, reward, done, _ = env.step(action)
        if perceive: perceive(observation, action, reward, nxt_observation, done)
        observation = nxt_observation
        ret += reward
        if done: return ret


def train_episodes(env, agent, n_episodes=500):
    rewards, aver_rewards = [], []
    try:
        for i_episode in range(n_episodes):
            # if i_episode % N_TEST == 0: play(env, agent.greedy_action, None, True)
            rewards.append(play(env, agent.epsilon_greedy, agent.perceive))

            aver_rewards.append(np.sum(rewards[-min(N_TEST, len(rewards)):]) / min(N_TEST, len(rewards)))
            print("Episode {} finished with test average reward {:.2f}".format(i_episode, aver_rewards[-1]))
            if len(rewards) > N_TEST and aver_rewards[-1] >= GOAL:
                print("Environment solved after {} episodes".format(i_episode))  # 按openai gym 要求完成了环境
                break
        else:
            print("Maximum {} of episodes exceeded".format(n_episodes))
    except KeyboardInterrupt:
        # 强行结束
        # pycharm不能用
        print('Training interrupted by KeyboardInterrupt at {}'.format(i_episode))
    finally:
        with open(agent.log_dir + 'rewards.pickle', 'wb') as f:
            pickle.dump((rewards, aver_rewards), f)

        # 画图
        plt.plot(rewards, label='Return for each episode')
        plt.plot(aver_rewards, label='Average return for last {} episodes'.format(N_TEST))
        plt.legend(frameon=False)
        plt.xlabel('Episode')
        plt.ylabel('Return')
        plt.show()


def main():
    env = gym.make(ENV_NAME)
    agent = dqn.DoubleFCQN(env, ENV_NAME)  # 三层隐藏层
    agent.save_hyperparameters()
    train_episodes(env, agent, MAX_EPISODES)


if __name__ == "__main__":
    main()
