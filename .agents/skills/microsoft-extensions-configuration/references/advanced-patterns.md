# Microsoft Extensions Configuration Advanced Patterns

Adapted from the upstream `dotnet-skills` `microsoft-extensions-configuration` skill and narrowed
for this repository's reusable slice format.

## Validators with dependencies

`IValidateOptions<T>` validators can use dependency injection when validation depends on
environment, logging, or other services.

```csharp
public sealed class DatabaseSettingsValidator : IValidateOptions<DatabaseSettings>
{
    private readonly IHostEnvironment environment;

    public DatabaseSettingsValidator(IHostEnvironment environment)
    {
        this.environment = environment;
    }

    public ValidateOptionsResult Validate(string? name, DatabaseSettings options)
    {
        var failures = new List<string>();

        if (string.IsNullOrWhiteSpace(options.ConnectionString))
        {
            failures.Add("ConnectionString is required.");
        }

        if (environment.IsProduction() &&
            options.ConnectionString?.Contains("localhost", StringComparison.OrdinalIgnoreCase) == true)
        {
            failures.Add("Production connection strings must not point to localhost.");
        }

        return failures.Count > 0
            ? ValidateOptionsResult.Fail(failures)
            : ValidateOptionsResult.Success;
    }
}
```

Use this pattern when Data Annotations are not expressive enough.

## Named options

Use named options when one settings type represents multiple independently configured instances.

```csharp
builder.Services.AddOptions<DatabaseSettings>("Primary")
    .BindConfiguration("Databases:Primary")
    .ValidateDataAnnotations()
    .ValidateOnStart();

builder.Services.AddOptions<DatabaseSettings>("Replica")
    .BindConfiguration("Databases:Replica")
    .ValidateDataAnnotations()
    .ValidateOnStart();
```

Consumer example:

```csharp
public sealed class DataService
{
    private readonly DatabaseSettings primary;
    private readonly DatabaseSettings replica;

    public DataService(IOptionsSnapshot<DatabaseSettings> options)
    {
        primary = options.Get("Primary");
        replica = options.Get("Replica");
    }
}
```

Keep named options explicit and use them only when multiple instances are a real requirement.

## Post-configuration

Use `PostConfigure` when normalization must happen after binding but before consumers rely on the
final settings shape.

```csharp
builder.Services.AddOptions<ApiSettings>()
    .BindConfiguration(ApiSettings.SectionName)
    .PostConfigure(options =>
    {
        if (!string.IsNullOrEmpty(options.BaseUrl) && !options.BaseUrl.EndsWith('/'))
        {
            options.BaseUrl += "/";
        }

        options.Timeout ??= TimeSpan.FromSeconds(30);
    })
    .ValidateDataAnnotations()
    .ValidateOnStart();
```

Use this for normalization and derived defaults, not to hide missing required settings.

## Testing validators

Treat `IValidateOptions<T>` implementations as plain classes with focused tests.

```csharp
public sealed class SmtpSettingsValidatorTests
{
    private readonly SmtpSettingsValidator validator = new();

    [Fact]
    public void Validate_with_valid_settings_returns_success()
    {
        var settings = new SmtpSettings
        {
            Host = "smtp.example.com",
            Port = 587,
            Username = "user@example.com",
            Password = "secret"
        };

        var result = validator.Validate(name: null, settings);

        Assert.True(result.Succeeded);
    }

    [Fact]
    public void Validate_with_missing_host_returns_failure()
    {
        var settings = new SmtpSettings { Host = "" };

        var result = validator.Validate(name: null, settings);

        Assert.False(result.Succeeded);
        Assert.Contains("Host", result.FailureMessage);
    }
}
```

Prefer focused validator tests over broad startup-only tests when the rules themselves are the
important behavior.
