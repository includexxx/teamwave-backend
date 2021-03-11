class StackOverFlow:
    endpoint = 'https://api.stackexchange.com/2.2/search/advanced?'

    def get_params(self):
        return ['page', 'pagesize', 'fromdate', 'todate', 'min', 'order', 'sort', 'q', 'max', 'accepted',
                'wiki', 'views', 'url', 'user', 'title', 'tagged', 'nottagged', 'notice', 'migrated',
                'closed', 'body', 'answers', 'site']

    def check_query_params(self, params):
        param_list = self.get_params()
        for p in params:
            if p not in param_list:
                return False

        return True

    def build_payload(self, query_params):
        url = self.endpoint
        for key in query_params:
            print(query_params[key])
            if query_params[key] in ['NaN', 'null']:
                continue
            url += ('&' + key + '=' + query_params[key])

        if "sort" not in query_params:
            url += '&sort=activity'
        if "site" not in query_params:
            url += '&site=stackoverflow'
        if "order" not in query_params:
            url += '&order=desc'
        return url
