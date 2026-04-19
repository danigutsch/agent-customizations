# Microsoft Extensions Dependency Injection Advanced Patterns

Adapted from the upstream `dotnet-skills` `microsoft-extensions-dependency-injection` skill and
narrowed for this repository's reusable slice format.

## Testing with production registration reuse

Prefer reusing production `Add*` extension methods in tests and overriding only what differs.

```csharp
var services = new ServiceCollection();

services
    .AddUserServices()
    .AddOrderServices();

services.AddSingleton<IClock, FakeClock>();
```

This keeps test composition close to production while making overrides explicit.

## Explicit scope creation in singleton-driven flows

Background services and other singleton-driven components must create scopes when they need scoped
services.

```csharp
public sealed class OrderWorker : BackgroundService
{
    private readonly IServiceScopeFactory scopeFactory;

    public OrderWorker(IServiceScopeFactory scopeFactory)
    {
        this.scopeFactory = scopeFactory;
    }

    protected override async Task ExecuteAsync(CancellationToken stoppingToken)
    {
        while (!stoppingToken.IsCancellationRequested)
        {
            using var scope = scopeFactory.CreateScope();
            var orderService = scope.ServiceProvider.GetRequiredService<IOrderService>();

            await orderService.ProcessNextAsync(stoppingToken);
        }
    }
}
```

Avoid capturing scoped dependencies directly in singleton constructors.

## Conditional and factory registration

Use explicit factories or conditional registration only when the application genuinely needs runtime
selection or conditional composition.

```csharp
services.AddSingleton<IMessagePublisher>(serviceProvider =>
{
    var environment = serviceProvider.GetRequiredService<IHostEnvironment>();
    return environment.IsDevelopment()
        ? new ConsoleMessagePublisher()
        : new BusMessagePublisher(serviceProvider.GetRequiredService<IBusClient>());
});
```

Keep factory logic small and easy to reason about. If it grows large, move it into a dedicated type.

## Keyed or named service composition

When multiple implementations of the same abstraction are required, keep selection explicit and
localized.

```csharp
services.AddKeyedSingleton<INotificationSender, EmailNotificationSender>("email");
services.AddKeyedSingleton<INotificationSender, SmsNotificationSender>("sms");
```

Use this pattern deliberately; do not introduce keyed complexity if one default service is enough.

## Layered composition

For larger applications, compose registration in layers only when the structure adds clarity.

```csharp
public static class ApplicationServiceCollectionExtensions
{
    public static IServiceCollection AddApplicationServices(this IServiceCollection services)
    {
        return services
            .AddUserServices()
            .AddOrderServices()
            .AddEmailServices();
    }
}
```

Layering should make composition easier to read, not harder to trace.
