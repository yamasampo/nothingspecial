""" Track functions that are called during a process and output their names and 
versions. This attempts to make it easier to reproduce an analysis and also to
reduce time to trace back my codes when publishing.
"""

def save_proc_setting_as_file(
        file_handle, 
        package_name: str, 
        proc_desc: str,
        start_time: str, 
        separator: str, 
        package_version: str = '', 
        *args, **kw_args
        ):
    """Write arguments or keyword arguments to a file. Values will be 
    separated by a given separator. 
    """
    output_lines = []
    # If arguments are given as a list
    if len(args) > 0:
        output_lines.append(separator.join(args))

    # If arguments are given as a dictionary
    if len(kw_args) > 0:
        for k, v in kw_args.items():
            output_lines.append(f'{k}{separator}{v}')

    # Write to file
    if package_version != '':
        print(f'Package name: {package_name} (version {package_version})\n', 
              file=file_handle)
    else:
        print(f'Package name: {package_name} (no version provided)\n', 
              file=file_handle)
    print(f'Process desc: {proc_desc}', file=file_handle)
    print(f'Start time: {start_time}.', file=file_handle)
    print('\nThis process runs under the following arguments.', 
          file=file_handle)
    
    print('\n[Input Arguments]', file=file_handle)
    print('\n'.join(output_lines), file=file_handle)

