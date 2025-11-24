[![PyPI status](https://img.shields.io/pypi/status/ansicolortags.svg)](https://pypi.python.org/pypi/ansicolortags/) 

# Apigee-Simple-Github-Pipeline

**This is not an official Google product.**<BR>This implementation is not an official Google product, nor is it part of an official Google product. Support is available on a best-effort basis via GitHub.

***

  

## Goal

Simple implementation for a CI/CD pipeline for Apigee using GitHub repository, 
[CI/CD with GitHub](https://docs.GitHub.com/ee/ci/introduction/) and the Apigee Maven Plugins.

The CICD pipeline includes:

- Git branch dependent Apigee environment selection and proxy naming to allow
  deployment of feature branches as separate proxies in the same environment
- Open API Specification (Swagger) static code analysis using [stoplight spectral](https://github.com/stoplightio/spectral)
- Static Apigee Proxy code analysis using [apigeelint](https://github.com/apigee/apigeelint)
- Static JS code analysis using [eslint](https://eslint.org/)
- Unit JS testing using [mocha](https://mochajs.org/)
- Integration testing of the deployed proxy using
  [apickli](https://github.com/apickli/apickli)
- Packaging and deployment of an Apigee configuration using
  [Apigee Config Maven Plugin](https://github.com/apigee/apigee-config-maven-plugin)
- Packaging and deployment of the API proxy bundle using
  [Apigee Deploy Maven Plugin](https://github.com/apigee/apigee-deploy-maven-plugin)


### API Proxy and Apigee configuration

The folder [./apiproxy](./apiproxy) includes a simple API proxy bundle, a simple Apigee configuration file [./EdgeConfig/edge.json](./EdgeConfig/edge.json) as well as the following resources:

- [GitHub Action Workflow File](.github/workflows/apigee-ci.yml) to define a GitHub Action CI
  multi-branch pipeline.
- [specs Folder](./specs) to hold the specification file for provided proxy.
- [test Folder](./test) to hold the specification (owasp ruleset), unit and integration tests.

## Target Audience

- Operations
- API Engineers
- Security

## Limitations & Requirements

  - The authentication to the Apigee Edge management API is done using OAuth2. If you require MFA, please see the [documentation](https://github.com/apigee/apigee-deploy-maven-plugin#oauth-and-two-factor-authentication) for the Maven deploy plugin for how to configure MFA.
  - The authentication to the Apigee X / Apigee hybrid management API is done using a GCP Service Account. See CI/CD Configuration [Instructions](https://gitlab.com/clalevee/apigee-simple-gitlab_ci-pipeline-v2#CI/CD-Configuration-Instructions).


## CI/CD Configuration Instructions

### Initialize a GitHub Repository

Create a GitHub repository to hold your API Proxy. 

To use the `Apigee-Simple-Github_CI-Pipeline`
in your GitHub repository like `github.com/my-user/my-api-proxy-repo`, follow these
steps:

```bash
git clone git@github.com:g-lalevee/Apigee-Simple-Github_CI-Pipeline.git
cd Apigee-Simple-Github_CI-Pipeline
git init
git remote add origin git@github.com:my-user/my-api-proxy.git
git checkout -b feature/cicd-pipeline
git add .
git commit -m "initial commit"
git push -u origin feature/cicd-pipeline
```

 

### GitHub Configuration 

Add GitHub secrets `APIGEE_CREDS_USR` and `APIGEE_CREDS_PSW`, to store your Apigee User ID and password:
- Go to your repository’s **Settings** > **Secrets**.
- Click the **New Repository Secret** button.<BR>Fill in the details:
  - Name: APIGEE_CREDS_USR
  - Value: your Apigee user ID 
  - Click the **Add secret** button
- Click again the **New Repository Secret** button.<BR>Fill in the details:
  - Name: APIGEE_CREDS_PSW
  - Value: your Apigee user ID password
  - Click the **Add secret** button

## Run the pipeline

Using your favorite IDE...
1.  Update the **.github/workflows/apigee-ci.yml** file.<BR>
In **"env"** section (workflow level), change `DEFAULT_APIGEE_ORG` value by your target Apigee organization.
2.  Read carefully the **"Set Variables for [Main] branch"** step to check if the multibranch rules match your GitHub and Apigee environment naming and configuration.
3. Save
4. Commit, Push.. et voila!

Use the GitHub UI to monitor your pipeline execution:

- Go to your GitHub repository > **Actions** (tab). You can see your workflow running.

![GitHub CICD Pipeline](img/GitHubUI-1.png)<BR>&nbsp;<BR>

- Click on it to see execution detail. In list of jobs, click on **Apigee-Deploy**.

![GitHub CICD Pipeline Animated](img/GitHubUI-2.png)<BR>&nbsp;<BR>

- At the end of execution, you can download artifacts.<BR>Click on **Summary** link and scroll down to the **Artifacts** section.

![GitHub CICD Pipeline artifacts](img/GitHubUI-3.png)<BR>&nbsp;<BR>

- For example, download **apigeelint-report.zip** file and open html content with your browser. You can see the results of static code analysis for Apigee proxy with Apigeelint tool:

![GitHub CICD Pipeline apickli](./img/GitHubUI-4.png)<BR>&nbsp;<BR>

---

### 1️⃣ “Use something that contains SYSGEN like SYSGEN123456789”

**Reply:**

> Updated all example MAL names to use the `SYSGEN123456789` style instead of simple numeric IDs.
> For example, the main MAL folder is now shown as `mal-SYSGEN123456789/`, and the sample product is `SYSGEN123456789-my-product.yaml`.

---

### 2️⃣ “Adding a new MAL – example MAL code (1234567)”

**Reply:**

> Adjusted the “Adding a new MAL” example to use a SYSGEN-style code.
> The onboarding doc now shows:
>
> * MAL folder: `mal-SYSGEN123456789/`
> * Proxy: `SYSGEN123456789-my-api`
> * Product: `SYSGEN123456789-my-product.yaml`.

---

### 3️⃣ “Only MALs that have changes is a little too broad”

**Reply:**

> Reworded this section to be more precise.
> It now reads along the lines of:
> *“Only MAL resources (proxies, products, KVMs, etc.) under MAL folders that changed in the PR are targeted by deployments (future optimisation – the current template just echoes what it would do).”*

---

### 4️⃣ “Prerequisites – not all API teams will have Products / API proxy must exist first”

**Reply:**

> Updated the onboarding prerequisites to separate the concepts:
>
> * Clarified that **a MAL code and owning GitHub team** are required.
> * Noted that having at least one **API proxy identified** is required before wiring products.
> * Marked product creation as a step that “may not apply to all API producer teams.”

---

### 5️⃣ “At least one API proxy and product identified” (wording)

**Reply:**

> Tweaked the prerequisite text as suggested:
>
> * It no longer assumes every team has a product on day one.
> * It now says that teams must identify **at least one API proxy** and optionally any initial products they plan to use.

---

### 6️⃣ “Emulate GitOps structure – products by org, etc.”

**Reply:**

> Clarified in the README that:
>
> * This repo is **application/MAL-focused**, not the platform GitOps repo.
> * Products are still org-level in Apigee, but in this repo they are grouped under `mal-<MAL_CODE>/products/` purely for **ownership and convenience**.
>   Also added a note that platform-level structure (org folders, sharedflows, etc.) stays in the enterprise GitOps repo.

---

### 7️⃣ “Deploy workflows do nothing – add guidance on checking Actions / SYS GEN in name”

**Reply:**

> Expanded the troubleshooting section for deploy workflows:
>
> * Stated explicitly that in this template the deploy workflows **only echo what they would do**.
> * Added guidance that, once real deployments are enabled, teams should verify runs via GitHub Actions and can filter by MAL/SYSGEN in the workflow or deployment name to find their runs.

---

### 8️⃣ “Looks amazing guys! See my comments.” (general wrap-up)

**Reply (top-level PR comment):**

> Thanks for the detailed review and suggestions.
> I’ve:
>
> * Switched all examples to use `SYSGEN123456789`-style IDs.
> * Clarified the MAL folder structure and env layout under each proxy.
> * Tightened the wording around “only MALs that changed” to focus on MAL resources affected by the PR.
> * Updated onboarding prerequisites around proxies vs. products.
> * Documented the separation between this application/MAL repo and the platform GitOps repo.
> * Expanded the troubleshooting text for deploy workflows as you suggested.
>   Please let me know if you’d like anything further refined.


### **🔍 Deployment Scope (Updated Per PR Review)**

**Only MAL resources that changed will be targeted by deployments.**  
Specifically, when a PR is merged, the workflow detects which  
`mal-<SYSGEN_CODE>/` folders were modified and limits deployment to:

- updated proxies  
- updated API products  
- updated KVMs  

> *Note: In this starter repository, the deployment workflow currently only  
> **echoes** what it would do. Actual deployment logic will be enabled later  
> as part of the enterprise GitOps integration.*

Hi all, I’ve pushed updates based on the PR feedback that was shared. Whenever you get a chance, please feel free to take a look and let me know if anything else is needed

Hey Ryan, I’ve pushed updates to the Apigee X PR based on Jeremy’s comments. Jeremy is not available, so whenever you have some time, could you please take a look and let me know if anything else is needed?






