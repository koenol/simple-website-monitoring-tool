"""ReportsManager handles report requests"""

import service

class ReportsManager:
    """Handles report requests"""
    def get_profile_reports(self, user_id, is_owner, pagination):
        """Get profile reports"""
        reports_page = pagination["page"]
        reports_limit = pagination["limit"]
        reports_offset = pagination["offset"]

        reports_count = service.get_count_website_reports_created(user_id)
        if is_owner:
            total_reports = service.get_user_websites_reports_count(user_id)
            reports = service.get_user_websites_reports_all(
                user_id, reports_limit, reports_offset
            )
        else:
            total_reports = service.get_user_websites_reports_count_public_only(user_id)
            reports = service.get_user_websites_reports_public_only(
                user_id, reports_limit, reports_offset
            )
        formatted_reports = service.format_reports_iso_to_readable_format(reports)
        reports_total_pages = service.calculate_total_pages(total_reports, reports_limit)
        return {
            "reports": formatted_reports,
            "reports_count": reports_count,
            "reports_page": reports_page,
            "reports_total_pages": reports_total_pages,
        }

    def get_website_reports(self, url_id, pagination):
        """Get website reports"""
        reports_page = pagination["page"]
        reports_limit = pagination["limit"]
        reports_offset = pagination["offset"]
        total_reports = service.count_website_reports_by_id(url_id)
        reports = service.get_website_reports_by_id(url_id, reports_limit, reports_offset)
        formatted_reports = service.format_reports_iso_to_readable_format(reports)
        reports_total_pages = service.calculate_total_pages(total_reports, reports_limit)
        return {
            "reports": formatted_reports,
            "reports_page": reports_page,
            "reports_total_pages": reports_total_pages,
        }
