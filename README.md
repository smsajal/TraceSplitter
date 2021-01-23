# TraceSplitter
## How to Run?

Run the `scalingMethods.py` file by defining the following variables in the main function
```
inputFile: the address of the original workload
scalingFactor: the scaling factor required, 0 < scalingFactor <= 1
bucket: for model based sampling, time bucket duration (second)
```

## ReqSizeEstimation

Modify `src/userDefinedMethods.reqSizeEstimation(requestSize,details)` function to get service time from `requestSize` and `opaqueData` from your workload respectively.

Example:
```python
'''
Example 1:
all the requests have same service time
'''
def reqSizeEstimation(size, details):
    return 1


'''
Example 2:
let, details can have request type in a social media application i.e. calue of details  can be LOGIN or POST or SEND_MESSAGE
'''

def reqSizeEstimation(requestSize,details):
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
arrivalTime, requestSize, details
```
The data type should be:
```
arrivalTime: arrival time of the request in nanoseconds (long int)
requestSize: size of the request (float)
details: any additional request information (string)
```
The workload should be in non-decreasing order of the arrival time. A sample workload is provided in _input_ directory.
