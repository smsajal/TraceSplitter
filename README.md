# TraceSplitter
## How to Run?


Run the `scalingMethods.py` file 

```bash
python3 scalingMethods.py --traceFile $trace_file_path --downscalingScheme $downscaling_scheme_name --bucket $bucket_value --scalingFactor $scaling_factor_value
```
__Example-1:__ To downscale a trace file `/dir1/dir2/tracefile.txt` with the downscaling scheme of `RRR` with scaling factor of `0.9`, the command would be:

```bash
python3 scalingMethods.py --traceFile /dir1/dir2/tracefile.txt --downscalingScheme RRR --scalingFactor 0.9
```

__Example-2:__ To downscale a trace file To downscale a trace file `/dir1/dir2/tracefile.txt` with the downscaling scheme of `avgRateScaling` with scaling factor of `0.7` and bucket of 10 millisecond, the command would be:

```bash
python3 scalingMethods.py --traceFile /dir1/dir2/tracefile.txt --downscalingScheme avgRateScaling --scalingFactor 0.7 --bucket 0.01
```



## Variables

__traceFile:__ The path of the original . This is a required parameter.

__downscalingScheme:__ The downscaling scheme to be used for downscaling trace. The choices are: avgRateScaling, tspan, randomSampling, RRR, RR and, LWL. This is an optional parameter with default value = LWL. (Details on downscaling schemes are described here.)

__scalingFactor:__ The scaling factor for downscaling trace, 0 < scalingFactor <= 1. This is an optional parameter with default value is 0.5

__bucket:__ This parameter is to specify the duration (seconds) of the bucket for `avgRateScaling` downscaling. This is an optional parameter with default value of 1.0

## Downscaling Schemes
__avgRateScaling:__ averages the number of requests in the specifies time bucket, and scales that according to the scaling factor. 

__tspan:__ time span scaling downscaling, downscales the arrival rate by spreading the requests across a longer time period.

__randomSampling:__ random sampling from the original trace file to get required number of requests.

__RRR:__ randomized round robin downscaling technique. For each request, the partition is selected at random.

__RR:__ Round robin downscaling technique. For each request, the partition is selected in a round robin style.

__LWL:__ Least work left downscaling technique. When assigning a request to a partition, the partition with the least work is selected.

## ReqSizeEstimation

Modify `src/userDefinedMethods.reqSizeEstimation(requestSize, details)` function to get service time from `requestSize` and `details` from your trace respectively.

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

The user should modify the function as they see fit to provide the most appropriate request size estimation for the requests in their trace.

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

The trace should be in non-decreasing order of the arrival time. A sample trace is provided in _input_ directory.
