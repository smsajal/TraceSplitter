# TraceSplitter
_TraceSplitter_ is published as a [research paper](https://sidsen.azurewebsites.net/papers/tracesplitter-eurosys21.pdf) in Sixteenth European Conference on Computer Systems [EuroSys '21](https://2021.eurosys.org/).

## Abstract



Realistic experimentation is a key component of systems research and industry prototyping, but experimental clusters are often too small to replay the high traffic rates found in production traces. Thus, it is often necessary to downscale traces to lower their arrival rate, and researchers/practitioners generally do this in an ad-hoc manner. For example, one practice is to multiply all arrival timestamps in a trace by a scaling factor to spread the load across a longer timespan. However, temporal patterns are skewed by this approach, which may lead to inappropriate conclusions about some system properties (e.g., the agility of auto-scaling). Another popular approach is to count the number of arrivals in fixed-sized time intervals and scale it according to some modeling assumptions. However, such approaches can eliminate or exaggerate the fine-grained burstiness in the trace depending on the time interval length.

The goal of this paper is to demonstrate the drawbacks of common downscaling techniques and propose new methods for realistically downscaling traces. We introduce a new paradigm for scaling traces that splits an original trace into multiple downscaled traces to accurately capture the characteristics of the original trace. Our key insight is that production traces are often generated by a cluster of service instances sitting behind a load balancer; by mimicking the load balancing used to split load across these instances, we can similarly split the production trace in a manner that captures the workload experienced by each service instance. Using production traces, synthetic traces, and a case study of an auto-scaling system, we identify and evaluate a variety of scenarios that show how our approach is superior to current approaches.


## Citing the Paper

You can use the following BibTex to cite the paper:


```
@inproceedings{sajal2021tracesplitter,
  title={TraceSplitter: a new paradigm for downscaling traces.},
  author={Sajal, Sultan Mahmud and Hasan, Rubaba and Zhu, Timothy and Urgaonkar, Bhuvan and Sen, Siddhartha},
  booktitle={EuroSys},
  pages={606--619},
  year={2021}
}

```




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
