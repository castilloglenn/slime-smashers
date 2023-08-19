import gym
import numpy as np
import tensorflow as tf

# Create the CartPole environment
env = gym.make("CartPole-v1")

# Define the Q-network model
model = tf.keras.Sequential(
    [
        tf.keras.layers.Dense(
            24, activation="relu", input_dim=env.observation_space.shape[0]
        ),
        tf.keras.layers.Dense(24, activation="relu"),
        tf.keras.layers.Dense(env.action_space.n, activation="linear"),
    ]
)

model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.001), loss="mse")

# Hyperparameters
epsilon = 1.0  # Exploration rate
epsilon_decay = 0.995
min_epsilon = 0.01
gamma = 0.99  # Discount factor
batch_size = 32

# Training the Q-network
for episode in range(1000):
    state = env.reset()
    done = False
    total_reward = 0

    while not done:
        if np.random.rand() < epsilon:
            action = env.action_space.sample()  # Exploration
        else:
            q_values = model.predict(np.array([state]))
            action = np.argmax(q_values)

        next_state, reward, done, _ = env.step(action)
        total_reward += reward

        # Update Q-values using Q-learning formula
        target = reward + gamma * np.max(model.predict(np.array([next_state])))
        q_values = model.predict(np.array([state]))
        q_values[0][action] = target
        model.fit(np.array([state]), q_values, verbose=0)

        state = next_state

    # Decay exploration rate
    epsilon = max(epsilon * epsilon_decay, min_epsilon)

    print(f"Episode: {episode+1}, Total Reward: {total_reward}")

# Test the trained agent
state = env.reset()
total_reward = 0
done = False

while not done:
    action = np.argmax(model.predict(np.array([state])))
    next_state, reward, done, _ = env.step(action)
    total_reward += reward
    state = next_state

print(f"Test Total Reward: {total_reward}")
