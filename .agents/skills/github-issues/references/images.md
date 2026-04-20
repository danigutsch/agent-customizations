# Images in Issues and Comments

How to embed images in GitHub issue bodies and comments programmatically.

## Methods

### 1. Contents API (recommended for private repos)

Push image files to a branch in the same repository, then reference them with a URL that works for
authenticated viewers.

```bash
# Get the SHA of the default branch
SHA=$(gh api repos/{owner}/{repo}/git/ref/heads/main --jq '.object.sha')

# Create a new branch
gh api repos/{owner}/{repo}/git/refs -X POST \
  -f ref="refs/heads/{username}/images" \
  -f sha="$SHA"
```

```bash
# Base64-encode the image and upload
BASE64=$(base64 -i /path/to/image.png)

gh api repos/{owner}/{repo}/contents/docs/images/my-image.png \
  -X PUT \
  -f message="Add image" \
  -f content="$BASE64" \
  -f branch="{username}/images" \
  --jq '.content.path'
```

Reference the image in Markdown:

```markdown
![Description](https://github.com/{owner}/{repo}/raw/{username}/images/docs/images/my-image.png)
```

Use the `github.com/{owner}/{repo}/raw/{branch}/{path}` format rather than
`raw.githubusercontent.com` for private repositories.

### 2. Browser upload

The most reliable permanent image URLs come from the GitHub web UI:

1. Open the issue or comment in a browser.
2. Drag and drop or paste the image into the editor.
3. GitHub generates a permanent `https://github.com/user-attachments/assets/{UUID}` URL.

There is no public API for generating `user-attachments` URLs.

## Common pitfalls

- `raw.githubusercontent.com` returns 404 for private repositories.
- Contents API `download_url` values are temporary.
- Browser-only asset upload endpoints require session cookies and CSRF tokens.
- Auth-required image URLs do not render in email notifications.
