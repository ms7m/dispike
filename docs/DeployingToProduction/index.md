# Deploying to Production

After completing development of your bot, and fully tested it in a controlled environment.. It's time to deploy it and allow requests from Discord.

For security reasons, Dispike does not **allow you to bind to any other address other than local**. This means that no one can access your bot unless it's coming from the machine itself. 

I highly recommend that you deploy behind a [reverse proxy](https://www.cloudflare.com/learning/cdn/glossary/reverse-proxy/). Not deploying behind a reverse proxy can result in degradation of user experience, security intrusions, etc. There are sample configurations provided here that can be used as a starting point for configuring your reverse proxy correctly. 

This guide will also provide links to some production-ready configurations for the most popular servers out there. Otherwise, it's recommended to read through the whole guide to understand -- and ultimately build the perfect configuration for your bot.



???+ info
    View a problem with a sample configuration? Proficient in a different reverse proxy server and don't see a configuration? Contribute to the docs to help out your fellow colleagues!



## Do I Need to use a Reverse Proxy?

99% of the time, it's the best choice. 

If your cloud provider/deployment service already provides services for load balancing and security

???+ warning
    Google Cloud App Engine and AWS Elastic Beanstalk =/= the typical servers that are under the same companies. These are specialized services that facilitate things like load balancing.

***



It's time to configure your workers.



***

