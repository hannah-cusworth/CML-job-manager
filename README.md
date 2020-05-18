# Job Manager 

This is a job management application which I build for my dad who works as a locksmith. You can try a demo of the application [here.](https://cml-job-manager.herokuapp.com/login)

### Adding jobs

The "New Job" form is intended for use primarily by clients. It consists of contact information, address details, job description, and an optional second address. Note that postcode and contact number fields must be valid. Upon creation, separate client, job and address objects will be created and associated in the database. 

### Job status

New jobs are assigned the status of "Inbox" upon creation so they can edited, supplimented or deleted as required before they become "Current". "Current" jobs can then be moved to "Archive" once they are completed. The status of all jobs can be changed from any page.

### Searching for jobs

Searches can be performed by client, address or job. All jobs can be found using the Search tab irrespective of their status. A job can also be found by searching by the associated client name or address detail. All fields return entries containing the search query. 

### Editing and deleting jobs 

Clicking on a job, client or address will open a details page. Once the "Edit" button is clicked, all elements in red are fully editable. Clicking this button again will save all changes without the need to refresh the page. 
To navigate between related objects, click on the related jobs/clients/addresss links (client/address pages), or on the Client/Adress headers (job pages).
Jobs can be deleted from the Inbox page, or from the Search page as long as the status is not "Current". Deleting a job will also cause the related client and address(es) to be deleted.

### Authentication

Authentication is required for all pages except the New Job form, as this is intended for use by the client. 

### Testing 

All server-side functionality is fully tested. Tests can be run using any of Django's standard test commands, which are documented [here.](https://docs.djangoproject.com/en/3.0/topics/testing/overview/)

