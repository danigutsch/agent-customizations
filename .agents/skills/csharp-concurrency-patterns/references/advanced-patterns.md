# C# Concurrency Patterns Advanced Examples

Adapted from the upstream `dotnet-skills` `csharp-concurrency-patterns` skill and narrowed for this
repository's reusable slice format.

## Bounded producer / consumer queues with channels

Use `Channel<T>` when producers and consumers need decoupling plus explicit backpressure.

```csharp
var channel = Channel.CreateBounded<WorkItem>(new BoundedChannelOptions(100)
{
    FullMode = BoundedChannelFullMode.Wait
});

public ValueTask EnqueueAsync(WorkItem item, CancellationToken cancellationToken) =>
    channel.Writer.WriteAsync(item, cancellationToken);

public async Task RunAsync(CancellationToken cancellationToken)
{
    await foreach (var item in channel.Reader.ReadAllAsync(cancellationToken))
    {
        await ProcessAsync(item, cancellationToken);
    }
}
```

Bounded channels are useful when producers can outrun consumers and memory growth must stay
controlled.

## Bounded fan-out with semaphores

Use bounded fan-out when independent async work must run concurrently without opening the floodgates.

```csharp
using var gate = new SemaphoreSlim(8);

var tasks = items.Select(async item =>
{
    await gate.WaitAsync(cancellationToken);
    try
    {
        await ProcessAsync(item, cancellationToken);
    }
    finally
    {
        gate.Release();
    }
});

await Task.WhenAll(tasks);
```

Prefer `Parallel.ForEachAsync` when it fits; use an explicit gate when the surrounding shape already
centers on task creation.

## Periodic background work with graceful shutdown

Prefer `PeriodicTimer` over manual sleep loops when repeated work should stop cleanly.

```csharp
public async Task RunAsync(CancellationToken cancellationToken)
{
    using var timer = new PeriodicTimer(TimeSpan.FromSeconds(30));

    while (await timer.WaitForNextTickAsync(cancellationToken))
    {
        await SyncAsync(cancellationToken);
    }
}
```

This keeps cancellation and repeated execution explicit without manual thread management.

## Serialized access instead of broad locking

When one mutable resource must be updated in order, serialize access through a channel-backed worker
instead of exposing the state to many callers.

```csharp
public sealed class CounterWorker
{
    private readonly Channel<int> channel = Channel.CreateUnbounded<int>();
    private int total;

    public ValueTask EnqueueAsync(int value, CancellationToken cancellationToken) =>
        channel.Writer.WriteAsync(value, cancellationToken);

    public async Task RunAsync(CancellationToken cancellationToken)
    {
        await foreach (var value in channel.Reader.ReadAllAsync(cancellationToken))
        {
            total += value;
        }
    }
}
```

This pattern reduces contention and makes the state owner obvious.
