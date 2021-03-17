
def person_filter(result):
    """Only keep the person detection data from the result's json"""
    data = []
    try:
        for algorithm in result['processing']:
            algorithm_data = {'algorithm': algorithm['algorithm']}
            person_data = []
            for detection in algorithm['detections']:
                frame = detection['frame']
                seconds = detection['seconds']
                if persons := detection['objects'].get('person'):
                    person_data.append(
                        {'frame': frame,
                         'seconds': seconds,
                         'persons': persons}
                    )
            algorithm_data['person_data'] = person_data
            data.append(algorithm_data)
    except KeyError as e:
        print(f'error: {e}')
    return {
        'id': result['filename'],
        'data': data
    }
