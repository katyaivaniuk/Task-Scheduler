## Why is a priority queue a particularly well-suited data structure to prioritize tasks?

Since a priority queue is a data structure used for maintaining the elements that have a particular priority associated with them, we need to understand that implementation of the priority queue with the use of heaps will be more time efficient than using the list. The reason behind this is that if we work with n elements and we need to insert them into list, we can do that in O(n) time since we might need to shift all the elements to find the right position of the element in the list, and then using the built-in function sort() to sort the list in the ascending order would result in time complexity of O(n log n). 

In comparison, implementing a priority queue with the use of heaps (specifically min heap) will result in time complexity of O(log n) for the element insertion using the method heappush() because we will insert the element at the last position available in a heap, and we might require to bubble it up to the root to restore the min-heap property, which requires the number of swaps proportional to the height of the heap, which is log n. Moreover, finding the minimum priority element in the min heap is O(1) since, referring to the min-heap property, the root element is the element with the lowest priority value. Suppose we want to extract the minimum priority element from the heap by using the method heappop(). In that case, we will pop the root element from the heap and put the last right-most element in a heap among the leaf nodes into the root position, and this might result in failing the min-heap property, which will require us to bubble the element all the down in the tree of height log n in the worst case scenario and will result in time complexity of O(log n) using heapify(). 

Since we should always consider data structures and algorithms that have a more efficient implementation in terms of time and space, we can derive the conclusion that using a priority queue implemented with a min-heap is more time efficient than using the list.To implement a task scheduler, we need to work with fixed-time and flexible-time tasks, which will require us to use two priority queues since their priority values will be calculated differently. In class Dependencies, I will calculate the priority for fixed-time tasks using the method priority_time_bound_task(), which will assign the priority of the fixed-time task based on its start time. This implies that the lower the number correspondng to the priority value, the higher prioriy it correspond to, the faster we should execute the task since it will have the earliest starting time. I will calculate the priority for flexible-time tasks in method priority_flexible() by taking into account all of the dependencies of the task (dependencies of dependencies), and the duration of the task. The fewer dependencies the flexible task has and the shorter its duration, the faster the task should be executed. The reason behind leaning towards flexible tasks with shorter duration is that people tend to procrastinate on longer tasks as they might be more difficult or require a bit more effort, and due to the “path of least resistance,” people choose smaller tasks to be completed first since it will generate the motivation for further task completion and will give the feeling of productivity. Therefore, as we can see, the smaller the number corresponding to the priority value, the earlier it should be executed, implying that Min Heap should be used for the algorithm implementation. 
