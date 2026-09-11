# Publish this repository

Suggested name: **panic-bomber-cd-builder**

Suggested description: **Build the tested Panic Bomber Neo Geo CD port from AES/MVS ROMs, using finalized CD audio.**

## Web interface

1. At <https://github.com/new>, select your account, enter the name and description, and choose the visibility you want.
2. Create an empty repository. Leave the automatic README, .gitignore and license options unchecked; the prepared files already include a README and ignore rules, and no new license choice has been made.
3. Extract `Panic-Bomber-CD-GitHub-Ready.zip` locally.
4. On the empty repository page, use **uploading an existing file**. Upload the contents of the extracted `panic-bomber-cd-builder` folder, preserving the `data`, `audio` and `docs` folders. Upload the files themselves, not the ZIP or its enclosing folder.
5. Include `.gitignore` and `.gitattributes`; if your file picker hides them, add them afterward with **Add file → Create new file**, copying their exact contents.
6. Commit the files with a message such as `Add Panic Bomber CD builder 1.0`.

## Add the complete download

1. Open **Releases → Draft a new release**.
2. Create tag `v1.0.0` targeting the repository's default branch.
3. Set the title to **Panic Bomber CD Builder 1.0**.
4. Copy the text from `docs/release-notes-v1.0.md` into the description.
5. Attach the existing **Panic-Bomber-CD-Builder-1.0.zip** (about 303 MB), which includes finalized music.
6. Publish the release when ready.

The large complete package belongs in a release asset, not the source file upload. Users then get a small source repository and a complete ready-to-run download.

## Git command line alternative

From the extracted repository folder, replace `YOUR-USERNAME` below with your actual account name:

```sh
git init -b main
git add .
git commit -m "Add Panic Bomber CD builder 1.0"
git remote add origin https://github.com/YOUR-USERNAME/panic-bomber-cd-builder.git
git push -u origin main
```

Use your normal GitHub sign-in flow. Do not place account tokens in project files.

Official documentation:
- <https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-new-repository>
- <https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github>
