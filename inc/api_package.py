import os
import logging
import apie
from flask import request

class package(apie.Endpoint):
    def __init__(this, name="Package API Endpoint"):
        super().__init__(name)

        this.allowedNext.append('upload')
        this.allowedNext.append('download')
        this.allowedNext.append('delete')
        this.allowedNext.append('list')

        # These should be provided by a predecessor.
        this.staticKWArgs.append('package_package_authenticator')
        this.staticKWArgs.append('package_upload_url')
        this.staticKWArgs.append('package_upload_query_map')
        this.staticKWArgs.append('package_upload_data_map')
        # upload_files is not static. downstream 'files' arg will grab.
        this.staticKWArgs.append('package_download_url')
        this.staticKWArgs.append('package_download_query_map')
        this.staticKWArgs.append('package_download_data_map')
        this.staticKWArgs.append('package_download_redirect_url_field')
        this.staticKWArgs.append('package_delete_url')
        this.staticKWArgs.append('package_delete_query_map')
        this.staticKWArgs.append('package_delete_data_map')
        this.staticKWArgs.append('package_list_url')
        this.staticKWArgs.append('package_list_query_map')
        this.staticKWArgs.append('package_list_data_map')

        this.optionalKWArgs['package_name'] = None
        this.optionalKWArgs['domain'] = ""
        this.optionalKWArgs['visibility'] = "public"
        this.optionalKWArgs['description'] = ""
        this.optionalKWArgs['type'] = ""
        this.optionalKWArgs['version'] = ""

        this.helpText = '''\
Perform CRUD operations, or more precisely LUDD operations (List, Upload, Download, Delete) on packages.
This will prepare all arguments for the generic LUDD endpoints.

You may also use this endpoint with http methods rather than next Endpoints.
For example curl -X GET .../package/list is the same as curl -X GET .../package, which is different from curl -X .../package?package_name=whatever_you_want
'''

    def Call(this):

        # Enable calling *this without a next. We'll figure out what to do by the nature of the request.
        if (not this.next):
            if (this.request.method in ['GET']):
                if (this.package_name):
                    this.next.append('download')
                else:
                    this.next.append('list')

            elif (this.request.method in ['POST', 'PUT', 'PATCH']):
                this.next.append('upload')

            elif (this.request.method in ['DELETE']):
                this.next.append('delete')


        # Set member variables so that they can be Fetch()ed by whatever is next.
        this.authenticator = this.package_authenticator
        this.method = this.request.method
        this.url = getattr(this, f"package_{this.next[0]}_url")
        this.query_map = getattr(this, f"package_{this.next[0]}_query_map")
        this.data_map = getattr(this, f"package_{this.next[0]}_data_map")

        if (this.next[0] == 'download'):
            this.redirect_url_field = this.download_redirect_url_field

