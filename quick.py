from vsbuilder import VSCommander

if __name__ == "__main__":
    try:
        command = VSCommander()
        command.run()
    except Exception as ex:
        print ex
