from typing import List, Dict
from collections import deque

class Task:
    """
    This is a Task class that stores the information about the instance of the task.  
    Attributes
    ----------
    id : integer
        This is the ID of the task, corresponding to the parameter id.
    time : integer
        This is the starting time of the task, corresponding to the parameter time.
    description : str
        This is the description of the task, corresponding to the parameter description.
    duration : integer
        This is the duration of the task, corresponding to the parameter duration.
    status : str
        This is status of the task, corresponding to the parameter status.
    priority : integer
        This is the priority of the task, corresponding to the parameter rotation_city .
    """
    def __init__(self, id: int, time: int, description: str, duration: int, dependencies: List[int], status: str, priority: int):
        
        self.id = id
        self.time = time
        self.description = description
        self.duration = duration
        self.dependencies = dependencies
        self.status = status
        self.priority = priority

   

    def __repr__(self):
        #return f"Task id: {self.id} priority: {self.priority}   \n"
        return f"Task ID : {self.id}, time : {self.time}, description : {self.description}, duration : {self.duration}, dependencies : {self.dependencies}, status : {self.status}, priority : {self.priority}"



class Dependencies:
    """ 
    A class that implements the methods for finding all the dependencies of the task (dependencies of dependencies), 
    and calculates priorities for the tasks dependending on whether they are fixed or flexible. 

    Attributes
    ----------
    task_map : dict
        A Python dictionary where key values are the IDs of the particular tasks, 
        and the values is the list of all the input attributes given 
        (id, start time, description, duration, dependencies, status and priority)

    """  

    def __init__(self, tasks: List[Task]):
        self.task_map = {task.id: task for task in tasks}


        
   #get dependencies of the dependencies in form of dictionary for all tasks 
    def get_all_dependencies(self) -> Dict[int, List[int]]:
        """
        Creating a dictionary where the key is the ID of the task, and values are the 
        list of all dependencies (dependencies of dependencies).

        Parameters
        ----------
        None

        Returns
        ----------
        Dict
            Dictionary where values are the lists of all the dependencies, and keys are the IDs of the tasks

        """
        res = {}
        for key in self.task_map.keys():
            res[key] = self.get_task_dependencies(key)
        return res



    def get_task_dependencies(self, id: int): #graph search 
        """
        Creating a list of all the dependencies of the task, meaning that it finds the dependencies of the initial dependencies
        using queue

        Parameters
        ----------
        ID: int
            ID of the task to gather the dependencies of

        Returns
        ----------
        List
            List containing all the dependencies of the given task

        """
        if self.task_map.get(id) is None:
            raise KeyError(f"No key with value {id}")
        result = [] 
        queue = deque(self.task_map.get(id).dependencies)
        while queue: 
            cur_id = queue.pop()
            result.append(cur_id)
            for dependency in self.task_map.get(cur_id).dependencies:
                queue.append(dependency)
        return result #list of all dependencies of dependencies of a particular task
   



    def priority_time_bound_task(self, tasks_map: Dict[int, List[int]]):
        """
        Creating a list of tuples where the first element corresponds to the priority of the time bound task based on the start time, and
        the second element is the ID of the time bound task. 

        Parameters
        ----------
        tasks_map: Dict
            Dictionary where the IDs of the task is a key, and values 
            are all the attributes given in the Task class (id, start time, description, dependencies, status, priority, duration)

        Returns
        ----------
        List
            List containing tuples of the form (priority based on the start time, ID) for the time bound tasks 

        """
        list_of_fixed_time_tasks = tasks_map.filter_time_bound_tasks(True)   #getting all the IDs of tasks that have fixed time 

        priority_list = [] #initializing list of tuples of form (priority based on the start time, id)
        tuples_list = []  #initializing list of tuples of form (starting time, id)

        for element in list_of_fixed_time_tasks:
            tuples_list.append((self.task_map[element].time, self.task_map[element].id)) #creating tuples of the form (start_time, id)
            
        for tuple_ in tuples_list:
            tuple_ = list(tuple_) #tuples are immutable, so we can't chaneg anything inside
            cur_priority = self.task_map[tuple_[1]].time 
            if self.task_map[tuple_[1]].priority == 0:
                self.task_map[tuple_[1]].priority = cur_priority
                priority_list.append((cur_priority, self.task_map[tuple_[1]].id)) 
                
        return priority_list



    def priority_flexible(self, dependencies: Dict[int, List[int]]):
        """
        Creating a list of tuples where the first element corresponds to the priority of the flexible task based on the number of dependencies and duration, and
        the second element is the ID of the flexible task. 

        Parameters
        ----------
        dependencies: Dict
            Dictionary where the IDs of the task is a key, and values are 
            all gathered dependencies (dependencies of dependencies)

        Returns
        ----------
        List
            List containing tuples of the form (priority based on the number of all dependencies and duration/1000000, ID) for the flexible tasks. 

        """
        input_tasks = self.task_map 
        flexible_tasks = {} #initializing dictionary where all the flexible tasks Ids will be keys, and list of dependencies will be values 
        list_of_priorities = []
        

        for i in input_tasks: 
            if self.task_map[i].priority == 0 and self.task_map[i].time == 0: #additional checks to we avoid duplicates 
                flexible_tasks[i] = self.get_task_dependencies(i)

        for key, dependencies in flexible_tasks.items(): 
            self.task_map[key].priority = len(dependencies) +  (self.task_map[key].duration)/100000
            list_of_priorities.append((self.task_map[key].priority, self.task_map[key].id))
            
        return list_of_priorities



class TaskMap:
    def __init__(self, tasks: List[Task]):
        self.task_map = {task.id: task for task in tasks}



    def filter_time_bound_tasks(self, time_bound: bool):
        """
        Getting tasks of interest: time bound or flexible tasks. 
        
        Parameters
        ----------
        time_bound: bool
            True or False depending on what kind of tasks we want to wotk with:

            True - executing time bound tasks
            False - executing flexible tasks

        Returns
        ----------
        List
            List containing IDs of either time bound tasks or flexible tasks.
        """
        result = []
        for id in self.task_map:
            
            if bool(self.task_map[id].time) == time_bound: # 0 corresponds to False, number greater than 0 correspond to True 
                result.append(self.task_map[id].id) 
                
        return result



class TaskScheduler:
    """
    A Simple Daily Task Scheduler that uses priority queues to execute the tasks scheduled for the day in the right order 
    
    Attributes
    ----------
    tasks : List
        List of all the given tasks with their attributes 

    task_map : Dict 
        A Python dictionary where key values are the IDs of the particular tasks, 
        and the values is the list of all the input attributes given 

    priority_queue_fixed : min heap 
        A priority queue of fixed time tasks that has the min heap structure 
        
    priority_queue_flexible : min heap
        A priority queue of flexible time tasks that has the min heap structure 
    """

    
    def __init__(self, tasks):
        self.tasks = tasks
        self.task_map = {task.id: task for task in tasks}
        self.priority_queue_fixed = MinHeapq()
        self.priority_queue_flexible = MinHeapq()
        self.id_list = [] #initializing the list of IDs to ensure that the code will work for the different inputs
    

    def create_heap_fixed(self, time_bound_tasks):
        """
        Creating min heap where the root node will be the fixed time task with the smallest priority 
        
        Parameters
        ----------
        time_bound_tasks: List
            List of IDs of fixed time tasks

        Returns
        ----------
        Heap
            Creates a min heap of the tuples of the form (priority of fixed time task, ID)
        """       
        for fixed_task in time_bound_tasks:
            self.priority_queue_fixed.heappush([self.task_map[fixed_task].priority, self.task_map[fixed_task].id])
        return self.priority_queue_fixed.heap


    def create_heap_flexible(self, flexible_tasks):
        """
        Creating min heap where the root node will be flexible task with the smallest priority 
        
        Parameters
        ----------
        flexible_tasks: List
            List of IDs of flexible time tasks

        Returns
        ----------
        Heap
            Creates a min heap of the tuples of the form (priority of flexible time task, ID)
        """ 
        for flex_task in flexible_tasks:
            self.priority_queue_flexible.heappush([self.task_map[flex_task].priority, self.task_map[flex_task].id]) 
        return self.priority_queue_flexible.heap
        

  
    def format_time(self, time):
        return f"{time//60}h{time%60:02d}"

    
    def run_task_scheduler(self, starting_time):
        """
        Creating the scheduler for the day, where the tasks will be executed based on their priority, and time gaps. 
        
        Parameters
        ----------
        starting_time: integer
            Integer representing when the day starts 

        Returns
        ----------
        Scheduler
            Creates a scheduler based on the order of task execution 
        """ 
        current_time = starting_time
        print("Running a simple scheduler:\n")

        #check whether the heap with the fixed-time tasks haven't exausted itself yet
        while len(self.priority_queue_fixed.heap) > 0:

            fixed_task = self.task_map[self.priority_queue_fixed.heappop()[1]]


            #check if the heap with flexible-time tasks is not empty yet
            #and whether the current time + duration of the first flexible task (on top of the min heap)
            #is less than the start of the fixed time task
            while len(self.priority_queue_flexible.heap) > 0 and current_time + self.task_map[self.priority_queue_flexible.mink()[1]].duration <= fixed_task.time:
                
                flexible_task = self.task_map[self.priority_queue_flexible.heappop()[1]] #pop the task with the particular ID under index 1 in the tuple of form (priority, ID)
                print(f" ⏰ t = {self.format_time(current_time)}")
                print(f"\t✨ Started executing task '{flexible_task.description}' for {flexible_task.duration} minutes")

                current_time += flexible_task.duration
                self.id_list.append((flexible_task.id, flexible_task.priority))
                flexible_task.status = "Completed"
                print(f"\t✅ t = {self.format_time(current_time)}, task {flexible_task.duration} completed with priority {flexible_task.priority}!\n") 

            print(f"\t⏳ You have a time gap of {fixed_task.time - current_time} minutes. Are there any tasks you forgot to include and need to do?")
            current_time = fixed_task.time
            print(f" ⏰  t = {self.format_time(current_time)}")
            print(f"\t✨ Started executing task '{fixed_task.description}' for {fixed_task.duration} minutes")
            current_time += fixed_task.duration
            self.id_list.append((fixed_task.id, fixed_task.priority))
            fixed_task.status = "Completed"
            print(f"\t✅ t = {self.format_time(current_time)}, task '{fixed_task.description}' completed with priority {fixed_task.priority}\n")
            
            #check whether the heap with the flexible tasks is not empty yet and pop elements out if there are no more 
            #fixed time tasks 
            while len(self.priority_queue_flexible.heap) > 0:

                flexible_task = self.task_map[self.priority_queue_flexible.heappop()[1]]  #popping the task with a particular ID which is under index 1 
                print(f" ⏰  t = {self.format_time(current_time)}")
                print(f"\t✨ Started task '{flexible_task.description}' for {flexible_task.duration} minutes")

                current_time += flexible_task.duration
                self.id_list.append((flexible_task.id, flexible_task.priority))
                flexible_task.status = "Completed"
                print(f"\t✅ t = {self.format_time(current_time)}, task '{flexible_task.description}' completed with priority {flexible_task.priority}\n") 
        
        print(f" ⏰  t = {self.format_time(current_time)} Finish time!")
        total_time = current_time - starting_time        
        print(f"\n🏁 Completed all planned tasks in {total_time//60}h{total_time%60:02d}min! You are done for the day 🎉")
        return self.id_list
    


                
                
def main():
    tasks = [ Task(id = 0, time = 0, description = "Prepare for work-study meeting", duration = 30, dependencies = [], status = "N", priority = 0),
        Task(id = 1, time = 540, description = "Have a work-study meeting with teammate Misha", duration = 45, dependencies =[0], status = "N", priority = 0),
        Task(id = 2, time = 0, description ="Dedicate time to revisit notes and do PCW for CS111", duration = 115, dependencies = [1], status = "N", priority = 0), 
        Task(id = 3, time = 1200, description ="Take CS111", duration = 90,dependencies = [2], status = "N", priority = 0), 
        Task(id = 4, time = 0, description = "Write a to-do list for the next day", duration = 15, dependencies =[0], status = "N", priority = 0), 
        Task(id = 5, time = 0, description = "Go to Drunken Moon Lake with friends",duration =  120, dependencies =[2, 4], status = "N", priority = 0), 
        Task(id = 6, time = 0, description = "Visit Baoan Temple near the residence hall", duration = 75, dependencies = [4], status = "N", priority = 0),
        Task(id = 7, time = 960, description = "Eat Taiwanese traditional food at the market", duration = 60, dependencies = [2, 6], status = "N", priority = 0)
    ]



    tasks_map = TaskMap(tasks)
    task_scheduler = TaskScheduler(tasks)

    time_bound_tasks = tasks_map.filter_time_bound_tasks(True)
    print("All fixed time tasks:", time_bound_tasks)


    flexible_tasks = tasks_map.filter_time_bound_tasks(False)
    print("All flexible time tasks:", flexible_tasks)

    dependencies_ = Dependencies(tasks)
    print("List of IDs of all dependendencies of the tasks", dependencies_.get_all_dependencies())

    time_bound_tasks_priorities = dependencies_.priority_time_bound_task(tasks_map)
    print("Priorities of time bound tasks", time_bound_tasks_priorities)

    flexible_tasks_priorities = dependencies_.priority_flexible(dependencies_)
    print("Priorities of flexible time tasks:", flexible_tasks_priorities)
    
    heap_fixed = task_scheduler.create_heap_fixed(time_bound_tasks)
    print("Heap created from fixed tasks", heap_fixed)

    heap_flexible = task_scheduler.create_heap_flexible(flexible_tasks)
    print("Heap created from flexible tasks", heap_flexible)

    start_scheduler = 8*60
    print(task_scheduler.run_task_scheduler(start_scheduler))
    



if __name__ == "__main__":
    main()
