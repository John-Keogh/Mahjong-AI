import os
import logging
from logging.handlers import RotatingFileHandler
import time

from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import DummyVecEnv, VecMonitor

from gamestate_env import MahjongEnv

# === Logging Setup ===
logger = logging.getLogger("train_discard_logger")
logger.setLevel(logging.INFO)

log_file_path = "logs/train_discard_logging.log"
os.makedirs(os.path.dirname(log_file_path), exist_ok=True)

file_handler = RotatingFileHandler(log_file_path, maxBytes=10*1024*1024, backupCount=5)
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(file_handler)

logger.info("=== Starting Mahjong discard model training ===")

# === Paths ===
model_name = "discard_model_v0"
model_path = f"models/{model_name}"
log_dir = f"logs/{model_name}"
os.makedirs(log_dir, exist_ok=True)

# === Environment Setup ===
env = DummyVecEnv([lambda: MahjongEnv()])
env = VecMonitor(env, filename=os.path.join(log_dir, "vec_monitor.csv"))

# === Model Setup ===
if os.path.exists(model_path + ".zip"):
    logger.info("Loading existing model...")
    model = PPO.load(model_path, env=env, device="cpu")
else:
    logger.info("Creating new model...")
    model = PPO("MlpPolicy", env, verbose=1, device="cpu")

# === Training ===
logger.info("Initialized PPO model.")
start_time = time.time()
model.learn(total_timesteps=1_000)
elapsed_time = time.time() - start_time
formatted_time = time.strftime('%H:%M:%S', time.gmtime(elapsed_time))
logger.info(f"Training complete. Duration: {formatted_time}")

# === Save model ===
model.save(model_path)
logger.info(f"Model saved to {model_path}")

# === Evaluation ===
logger.info("Starting evaluation episode.")
test_env = MahjongEnv()
obs, _ = test_env.reset()
done = False

print("Initial hand:")
test_env.render()

while not done:
    action, _ = model.predict(obs)
    obs, reward, terminated, truncated, info = test_env.step(action)
    done = terminated or truncated

print("Final hand:")
test_env.render()
logger.info("Evaluation complete.")
