import dtlpy as dl

if dl.token_expired():
    dl.login()


def copyItem(item: dl.Item):
    source_folder = item.dir
    destination_folder = item.dir
    destination_dataset_name = 'Target'
    copy_annotations = True
    flat_copy = False
    dataset_to = item.project.datasets.get(dataset_name=destination_dataset_name)
    # Download item (without save to disk)
    buffer = item.download(save_locally=False)
    # Give the item's name to the buffer
    if flat_copy:
        buffer.name = item.name
    else:
        buffer.name = item.filename[len(source_folder) + 1:]
    # Upload item
    print("Going to add {} to {} dir".format(buffer.name, destination_folder))
    new_item = dataset_to.items.upload(local_path=buffer, remote_path=destination_folder)
    if not isinstance(new_item, dl.Item):
        print('The file {} could not be upload to {}'.format(buffer.name, destination_folder))
        return
    print("{} has been uploaded".format(new_item.filename))
    if copy_annotations:
        new_item.annotations.upload(item.annotations.list())


# Use an existing project
project = dl.projects.get(project_name='TestingProject')
dataset = project.datasets.get(dataset_name='Source')
items = dataset.items.get_all_items()

# For Testing The Function
# for item in items:
#     copyItem(item)


service = project.services.deploy(func=copyItem,
                                  service_name='copy-item')
trigger = service.triggers.create(name='copying-items-to-target',
                                  function_name='copyItem',
                                  execution_mode=dl.TriggerExecutionMode.ALWAYS,
                                  resource=dl.TriggerResource.ITEM,
                                  actions=dl.TriggerAction.CREATED)


