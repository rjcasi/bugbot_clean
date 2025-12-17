import plotly.graph_objs as go

def count_inversions(a):
    inv = 0
    for i in range(len(a)):
        for j in range(i+1, len(a)):
            if a[i] > a[j]:
                inv += 1
    return inv

def quicksort_animation(arr):
    frames, entropy, annotations = [], [], []
    
    def quicksort(a, low, high):
        if low < high:
            p = partition(a, low, high)
            frames.append(go.Frame(data=[go.Bar(y=a)]))
            entropy.append(count_inversions(a))
            annotations.append(f"Pivot={a[p]} placed at index {p}")
            quicksort(a, low, p-1)
            quicksort(a, p+1, high)
    
    def partition(a, low, high):
        pivot = a[high]
        i = low
        for j in range(low, high):
            if a[j] < pivot:
                a[i], a[j] = a[j], a[i]
                i += 1
        a[i], a[high] = a[high], a[i]
        return i
    
    quicksort(arr, 0, len(arr)-1)
    return frames, entropy, annotations


def mergesort_animation(arr):
    frames, entropy, annotations = [], [], []
    
    def mergesort(a):
        if len(a) > 1:
            mid = len(a)//2
            L, R = a[:mid], a[mid:]
            mergesort(L)
            mergesort(R)
            i = j = k = 0
            merge_ops = []
            while i < len(L) and j < len(R):
                if L[i] < R[j]:
                    a[k] = L[i]; merge_ops.append(f"{L[i]} dropped at {k}"); i += 1
                else:
                    a[k] = R[j]; merge_ops.append(f"{R[j]} dropped at {k}"); j += 1
                k += 1
            while i < len(L):
                a[k] = L[i]; merge_ops.append(f"{L[i]} dropped at {k}"); i += 1; k += 1
            while j < len(R):
                a[k] = R[j]; merge_ops.append(f"{R[j]} dropped at {k}"); j += 1; k += 1
            frames.append(go.Frame(data=[go.Bar(y=a)]))
            entropy.append(count_inversions(a))
            annotations.append(", ".join(merge_ops))
    
    mergesort(arr)
    return frames, entropy, annotations