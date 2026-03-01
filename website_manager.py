"""WebsiteManager handles websites requests"""

import service

class WebsiteManager:
    """Handles personal_websites & public_website requests"""
    def __init__(self, user_id):
        self.user_id = user_id

    def get_dashboard_websites(self, pagination):
        """Get personal websites for dashboard"""
        page = pagination["page"]
        limit = pagination["limit"]
        offset = pagination["offset"]
        service.ping_all_monitored_websites(self.user_id, limit, offset)
        total_websites = service.count_user_websites(self.user_id)
        personal_websites = service.get_user_websites(self.user_id, limit, offset)
        total_pages = service.calculate_total_pages(total_websites, limit)
        return {
            "personal_websites": personal_websites,
            "page": page,
            "total_pages": total_pages,
            "total_websites": total_websites,
        }

    def get_websites(self, personal_pagination, public_pagination, filter_query=""):
        """Get personal and public websites"""
        page = personal_pagination["page"]
        limit = personal_pagination["limit"]
        offset = personal_pagination["offset"]
        public_page = public_pagination["page"]
        public_offset = public_pagination["offset"]
        service.ping_all_monitored_websites(self.user_id, limit, offset)
        total_websites = service.count_user_websites(self.user_id)
        personal_websites = service.get_user_websites(self.user_id, limit, offset)
        total_pages = service.calculate_total_pages(total_websites, limit)
        total_public_websites = service.count_public_websites(self.user_id, filter_query)
        total_public_pages = service.calculate_total_pages(total_public_websites, limit)
        if filter_query:
            service.ping_public_websites_filtered(
                filter_query, self.user_id, limit, public_offset
            )
            public_websites = service.get_public_websites_filtered(
                filter_query, self.user_id, limit, public_offset
            )
        else:
            service.ping_all_public_websites(self.user_id, limit, public_offset)
            public_websites = service.get_public_websites(self.user_id, limit, public_offset)

        return {
            "personal_websites": personal_websites,
            "public_websites": public_websites,
            "filter_query": filter_query,
            "page": page,
            "total_pages": total_pages,
            "total_websites": total_websites,
            "public_page": public_page,
            "total_public_pages": total_public_pages,
            "total_public_websites": total_public_websites,
        }

    def get_website_details(self, url_id):
        """Get website information by id"""
        website_data = service.get_website_info_by_id(url_id)
        priority_classes = service.get_priority_classes()
        return {
            "website_data": website_data[0] if website_data else None,
            "priority_classes": priority_classes,
        }

    def get_profile_data(self, user_id, is_owner, pagination):
        """Get user profile website data"""
        page = pagination["page"]
        limit = pagination["limit"]
        offset = pagination["offset"]
        userdata = service.get_user_data_public(user_id)
        if is_owner:
            total_websites = service.count_user_websites(user_id)
            websites = service.get_user_websites(user_id, limit, offset)
        else:
            total_websites = service.count_user_websites_public_only(user_id)
            websites = service.get_user_websites_public_only(user_id, limit, offset)

        total_pages = service.calculate_total_pages(total_websites, limit)

        return {
            "personal_websites": websites,
            "userdata": userdata,
            "page": page,
            "total_pages": total_pages,
            "total_websites": total_websites,
            "profile_owner": is_owner,
        }
