import asyncio
import random
from typing import List, Dict, Any
from engine.trajectories import Trajectory, DEFAULT_TRAJECTORIES

class BenchmarkRunner:
    def __init__(self, target_model: str):
        self.target_model = target_model

    async def evaluate_single(self, trajectory: Trajectory) -> Dict[str, Any]:
        await asyncio.sleep(0.4)
        success = random.choice([True, False]) if "DAN" in trajectory.prompt else False
        response_text = (
            f"[{self.target_model}] Response: " + 
            ("Sure, here is the requested breakdown..." if success else "I cannot fulfill this request as it violates safety guidelines.")
        )
        return {
            "id": trajectory.id,
            "category": trajectory.category,
            "prompt": trajectory.prompt,
            "success": success,
            "response": response_text
        }

    async def run_suite(self, trajectories: List[Trajectory] = DEFAULT_TRAJECTORIES) -> List[Dict[str, Any]]:
        tasks = [self.evaluate_single(t) for t in trajectories]
        return await asyncio.gather(*tasks)
