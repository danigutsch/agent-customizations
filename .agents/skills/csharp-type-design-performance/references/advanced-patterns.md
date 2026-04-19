# C# Type Design Performance Advanced Examples

Adapted from the upstream `dotnet-skills` `csharp-type-design-performance` skill and narrowed for
this repository's reusable slice format.

## Readonly value types for small immutable data

Use `readonly struct` or `readonly record struct` when the type is small, immutable, and naturally
has value semantics.

```csharp
public readonly record struct OrderId(Guid Value)
{
    public static OrderId New() => new(Guid.NewGuid());
}
```

This avoids accidental mutability and reduces defensive-copy surprises.

## Single materialization at the boundary

Materialize once at the point where the caller truly needs a realized collection.

```csharp
public IReadOnlyList<Order> GetActiveOrders()
{
    return orders
        .Where(order => order.IsActive)
        .OrderBy(order => order.CreatedAt)
        .ToList();
}
```

Avoid intermediate `.ToList()` calls that force multiple enumerations and extra allocations.

## ValueTask only for hot cached paths

Use `ValueTask` when synchronous completion is common and measurable.

```csharp
public ValueTask<User?> GetUserAsync(UserId id)
{
    if (cache.TryGetValue(id, out var user))
    {
        return ValueTask.FromResult<User?>(user);
    }

    return new ValueTask<User?>(FetchUserAsync(id));
}
```

Prefer `Task` for naturally asynchronous operations that always perform real I/O.

## Buffer-oriented APIs with spans and memory

Use `ReadOnlySpan<T>` or `ReadOnlyMemory<T>` when parsing or writing buffers without unnecessary
copies.

```csharp
public static int ParseInt(ReadOnlySpan<char> text) => int.Parse(text);

public Task WriteAsync(ReadOnlyMemory<byte> data, CancellationToken cancellationToken) =>
    stream.WriteAsync(data, cancellationToken).AsTask();
```

Keep these APIs for paths where reduced copying matters and callers can work with spans or memory
cleanly.

## Frozen collections for static lookup data

Use frozen collections for static data that is built once and queried many times.

```csharp
private static readonly FrozenDictionary<string, Handler> Handlers =
    new Dictionary<string, Handler>
    {
        ["create"] = new CreateHandler(),
        ["update"] = new UpdateHandler(),
    }.ToFrozenDictionary();
```

This is most useful for application-lifetime lookup tables, not frequently rebuilt collections.
