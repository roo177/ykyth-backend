class ListConvertToGenarator:

    @staticmethod
    def list_to_generator(lst):
        gen = (gn for gn in lst)
        return gen