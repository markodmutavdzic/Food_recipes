import clearbit

clearbit.key = 'sk_8da54fa427b2bd0d6cd83e87b13a06b8'


def additional_data(email):
    response = clearbit.Enrichment.find(email=email, stream=True)
    user_additional_data = {}

    if response['person'] is not None:
        user_additional_data['user_location'] = response['person']['location']
        user_additional_data['user_title'] = response['person']['employment']['title']
    else:
        user_additional_data['user_location'] = None
        user_additional_data['user_title'] = None

    if response['company'] is not None:
        user_additional_data['company_name'] = response['company']['name']
        user_additional_data['company_sector'] = response['company']['category']['sector']
    else:
        user_additional_data['company_name'] = None
        user_additional_data['company_sector'] = None

    return user_additional_data
