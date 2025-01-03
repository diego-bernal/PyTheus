"""
Basic parallel execution module for Pytheus.

This is a naive implementation of multi-threading that simply runs the same configuration 
multiple times in parallel. A better implementation would:

1. Distribute the number of samples evenly across threads
2. Generate output files in the same output folder
3. Compare against a shared best.json whenever a new solution is found

Classes:
    ParallelRunner: Manages parallel execution of Pytheus runs
"""

import threading
import time  # Add time for debugging
from typing import Optional
from .main import run_main
import logging

log = logging.getLogger(__name__)

class ParallelRunner:
    """
    Handles parallel execution of multiple Pytheus runs.
    
    This class creates multiple threads that each execute the same configuration file
    independently. Each thread will generate its own output folder and files.
    
    Parameters
    ----------
    config_file : str
        Path to the configuration JSON file to execute
    num_threads : int
        Number of parallel threads to spawn
    example : bool
        Whether the config file is an example from the package
        
    Methods
    -------
    run()
        Starts the parallel execution and waits for all threads to complete
    """
    
    def __init__(self, config_file: str, num_threads: int, example: bool = False):
        self.config_file = config_file
        self.num_threads = num_threads
        self.example = example
        self.threads = []
        self.lock = threading.Lock()
        print(f"\n=== Starting parallel execution with {num_threads} threads ===\n")

    def run(self) -> None:
        """
        Launches the parallel execution of Pytheus runs.
        
        Creates num_threads threads that each execute run_main() with the same
        configuration file. Waits for all threads to complete before returning.
        """
        print("Starting parallel execution")
        
        # Create and start threads with some delay between them
        for i in range(self.num_threads):
            thread = threading.Thread(
                target=self._worker_run,
                args=(i,),
                name=f"PytheusThread-{i}"
            )
            self.threads.append(thread)
            with self.lock:
                print(f"\n>>> Starting worker {i} <<<\n")
            thread.start()
            time.sleep(1)  # Small delay between thread starts
            
        # Wait for all threads to complete
        for i, thread in enumerate(self.threads):
            thread.join()
            with self.lock:
                print(f"\n>>> Worker {i} completed <<<\n")

    def _worker_run(self, worker_id: int) -> None:
        """Worker thread function that executes the main run
        
        Parameters
        ----------
        worker_id : int
            ID of the worker thread
        """
        with self.lock:
            print(f"\n>>> Worker {worker_id} executing <<<")
        
        try:
            # Run main with thread ID
            run_main(self.config_file, self.example)
            with self.lock:
                print(f"\n>>> Worker {worker_id} finished successfully <<<\n")
            
        except Exception as e:
            with self.lock:
                print(f"\n>>> Worker {worker_id} failed with error: {str(e)} <<<\n")
            raise

def run_parallel(config_file: str, num_threads: int, example: bool = False) -> None:
    """
    Entry point for parallel execution of Pytheus runs.
    
    Parameters
    ----------
    config_file : str
        Path to configuration JSON file
    num_threads : int 
        Number of threads to use
    example : bool, optional
        Whether config_file is an example from package, by default False
    """
    runner = ParallelRunner(config_file, num_threads, example)
    runner.run()
