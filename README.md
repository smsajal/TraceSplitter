# TraceSplitter
## How to Run?


Run the `scalingMethods.py` file 
```
python3 scalingMethods.py $inputFile $scalingFactor $bucket
```

The variables are the following:

__inputFile:__ the address of the original workload

__scalingFactor:__ the scaling factor required, 0 < scalingFactor <= 1

__bucket:__ for model based sampling, time bucket duration (second)


## ReqSizeEstimation

Modify `src/userDefinedMethods.reqSizeEstimation(requestSize,details)` function to get service time from `requestSize` and `details` from your workload respectively.

Example:
```python
'''
Example 1:
all the requests have same service time
'''
def reqSizeEstimation(requestSize, details):
    return 1


'''
Example 2:
details can have request type in a social media application i.e. value of details can be LOGIN or POST or SEND_MESSAGE
'''

def reqSizeEstimation(requestSize, details):
    if details=="LOGIN":
        return requestSize*2
    elif details=="POST":
        return requestSize*5/3
    else:
        return requestSize
    
```
## Trace File Format

The trace file should be of the following format:

```
arrivalTime,requestSize,details
```
The data type should be:
```
arrivalTime: arrival time of the request in nanoseconds (long int)
requestSize: size of the request (float)
details: any additional request information (string)
```
The workload should be in non-decreasing order of the arrival time. A sample workload is provided in _input_ directory.
