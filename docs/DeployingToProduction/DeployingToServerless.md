# Deploying to 'Serverless' platforms.

Since dispike is a normal AGSI application under the hood, you should have no compatibility issues using 'serverless' platforms such as 

- Amazon Lambda (using an adapter such as [magnum](https://github.com/jordaneremieff/mangum))
- Google Cloud App Engine (flex and standard environements)
- [Vercel](https://vercel.com/docs/runtimes#advanced-usage/advanced-python-usage)
- Heroku

Configuration and documentation can be found all over the internet (Search for FastAPI).. 

# Reminder

- AGSI entry point is hosted under ``.referenced_application`` attribute for your main bot.

- You may need to instruct Dispike to bind to 0.0.0.0!

***

# Deploying to AWS Lambda 

## Resources

- https://towardsdatascience.com/fastapi-aws-robust-api-part-1-f67ae47390f9

- https://github.com/iwpnd/fastapi-aws-lambda-example

# Deploying to Google Cloud App Engine 

## Resources

- https://medium.com/analytics-vidhya/deploying-fastapi-application-in-google-app-engine-in-standard-environment-dc061d3277a

- https://github.com/tiangolo/fastapi/issues/228

  

# Deploying to Vercel

## Resources

- https://blog.logrocket.com/deploying-fastapi-applications-to-vercel/
- https://github.com/benfasoli/vercel-fastapi

# Deploying to Heroku

- https://towardsdatascience.com/how-to-deploy-your-fastapi-app-on-heroku-for-free-8d4271a4ab9
- https://towardsdatascience.com/autodeploy-fastapi-app-to-heroku-via-git-in-these-5-easy-steps-8c7958ef5d41
- https://github.com/ms7m/dispike/pull/35#issue-607374151

