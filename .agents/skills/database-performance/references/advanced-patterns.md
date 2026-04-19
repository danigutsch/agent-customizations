# Database Performance Advanced Examples

Adapted from the upstream `dotnet-skills` `database-performance` skill and narrowed for this
repository's reusable slice format.

## Projection-first EF Core reads

Project directly into the DTO or summary shape the caller needs.

```csharp
public Task<IReadOnlyList<OrderSummary>> GetRecentOrdersAsync(int limit, CancellationToken cancellationToken) =>
    dbContext.Orders
        .AsNoTracking()
        .OrderByDescending(order => order.CreatedAt)
        .Take(limit)
        .Select(order => new OrderSummary(order.Id, order.Total, order.Status, order.CreatedAt))
        .ToListAsync(cancellationToken);
```

This avoids hydrating full entities and keeps the result shape tight.

## Split queries for wide related graphs

Use split queries when multiple includes would otherwise multiply rows excessively.

```csharp
var product = await dbContext.Products
    .AsNoTracking()
    .AsSplitQuery()
    .Include(product => product.Reviews)
    .Include(product => product.Images)
    .Include(product => product.Categories)
    .FirstOrDefaultAsync(product => product.Id == id, cancellationToken);
```

This trades one oversized cartesian result for multiple smaller focused queries.

## Batched reads instead of N+1 loops

Fetch related data in batches instead of issuing one query per parent row.

```csharp
var orders = await dbContext.Orders
    .AsNoTracking()
    .Where(order => order.CustomerId == customerId)
    .Take(limit)
    .ToListAsync(cancellationToken);

var orderIds = orders.Select(order => order.Id).ToList();

var items = await dbContext.OrderItems
    .AsNoTracking()
    .Where(item => orderIds.Contains(item.OrderId))
    .ToListAsync(cancellationToken);
```

The join back to parents can happen in memory because the related rows were already fetched in one
bounded batch.

## EF Core for writes, Dapper for read-heavy projections

A mixed approach can keep tracked writes ergonomic while making read-heavy projections explicit.

```csharp
const string sql = """
    SELECT id, customer_id, total, status, created_at
    FROM orders
    WHERE customer_id = @CustomerId
    ORDER BY created_at DESC
    LIMIT @Limit
    """;

var rows = await connection.QueryAsync<OrderSummaryRow>(
    sql,
    new { CustomerId = customerId, Limit = limit });
```

Use this pattern when a read model is clearer as SQL than as a large ORM expression tree.
