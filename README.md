# interop-aws-reporter

A reporting tool project based on the [RedHatQE/cloudwash](https://github.com/RedHatQE/cloudwash) cli.

This tool creates a Slack message report (with an attached HTML file), containing the data of OCP resources left in a given AWS account.

Reporting is done directly to a [configured Slack channel](#slack-channel-configuration) using `SlackAPI` or a Slack Webhook url.

## Content

- [Slack channel configuration](#slack-channel-configuration)
  - [Using with webhook url](#using-a-post-request-with-a-webhook-url)
  - [Using with SlackAPI](#using-a-slackapi-application-bot)
- [Local usage](#local-usage)
  - [Setup VirtualEnv](#setup-virtualenv)
  - [Execute](#execute)
- [Using in Openshift-Ci](#using-in-openshift-ci)

## Slack channel configuration

Once the reporting Slack channel has been set up, an activation must be done using either a webhook url, or a SlackAPI application bot.

For both methods, you need to create an app for the reporting tool, such as `my-project-cw-reporter`.

### Using a post request with a webhook url

- Create a new app using: https://api.slack.com/apps
- Generate a new webhook url for the reporting channel, by following this tutorial: https://api.slack.com/messaging/webhooks
- Once activated, make sure you're able to send messages like this:

    `curl -X POST -H 'Content-type: application/json' --data '{"text":"Hello, World!"}' <your-slack-webhook-url>`

### Using a SlackAPI application bot

- Create a new app using: https://api.slack.com/apps
- Generate an application token for your app, by following this tutorial: https://api.slack.com/authentication/oauth-v2#obtaining
- Once the token is set up, you need to update the `Bot Token Scopes` with:
  - [incoming-webhook](https://api.slack.com/scopes/incoming-webhook)
  - [files:write](https://api.slack.com/scopes/files:write)
  - [chat:write](https://api.slack.com/scopes/chat:write)
  - _Requesting permissions tutorial:_
    1. Open the settings for your app from the App Management page
    2. In the navigation menu, select `OAuth & Permissions`
    3. Scroll down to the Scopes section, and pick the desired permission (for example: `chat:write`) from the drop-down menu
    4. Save changes
    5. Reinstall app if needed

    **Learn more on: [Requesting permissions](https://api.slack.com/messaging/sending#permissions)**

## Local usage

#### Setup VirtualEnv

Use [poetry](https://python-poetry.org/docs/) to manage virtualenv.

```bash
pip install poetry
```

#### Execute

To run locally you can export the following environment variables:

```bash
poetry install

export CLEANUP_AWS__AUTH__ACCESS_KEY=<aws-access-key>  # AWS access key ID
export CLEANUP_AWS__AUTH__SECRET_KEY=<aws-secret-key>  # AWS secret key
export CLEANUP_AWS__AUTH__REGIONS='["all"]'   # Optional; set the list of regions for reporting
export CLEANUP_AWS__CRITERIA__OCPS__OCP_CLIENT_REGION=<For more info check out: https://github.com/RedHatQE/cloudwash/blob/master/README.md>
export CLEANUP_AWS__CRITERIA__OCPS__SLA=3d  # Optional; set the reporting SLA time for filtering resources

export CHANNEL_ID=<slack-channel-id>
export SLACK_BOT_TOKEN=<slack-bot-token>

poetry run python3 interop_aws_reporter/app.py
```

## Using in Openshift-Ci

The interop-aws-reporter tool is a containerized project which can be easily integrated into the [openshift/release](https://github.com/openshift/release) repo.

Running periodic job for reporting on a daily/weekly/monthly/yearly basis in OpenShift CI is very simple, you can do one of the following:

- Set the following secrets in your job's credentials files that required by the tool:
    - `slack-webhook-url`
    - `aws-access-key`
    - `aws-secret-key`
    - `channel-id`
    - `slack-bot-token`
- Create a config file for running the job using a cron value.
  - See [Example config file](https://github.com/openshift/release/blob/master/ci-operator/config/CSPI-QE/interop-aws-reporter/CSPI-QE-interop-aws-reporter-main__weekly_trigger.yaml)
- Add the [mpiit-interop-aws-reporter-ref](https://steps.ci.openshift.org/reference/mpiit-interop-aws-reporter) ref as the test step in your config

For adding optional variables to the job's, check out the [cloudwash docs](https://github.com/RedHatQE/cloudwash/blob/master/README.md).

Additional env variables for the tool can be set in the job's config file.
