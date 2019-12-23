import unittest
from traceback import print_tb
from ml_model_abc import MLModel
from model_stream_processor.model_manager import ModelManager


# creating an MLModel class to test with
class MLModelMock(MLModel):
    # accessing the package metadata
    display_name = "display name"
    qualified_name = "qualified_name"
    description = "description"
    major_version = 1
    minor_version = 1
    input_schema = None
    output_schema = None

    def __init__(self):
        pass

    def predict(self, data):
        pass


# creating a mockup class to test with
class SomeClass(object):
    pass


class ModelManagerTests(unittest.TestCase):

    def test1(self):
        """ testing the load_models() method """
        # arrange
        # instantiating the model manager class
        model_manager = ModelManager()
        # loading the MLModel objects from configuration
        model_manager.load_models(configuration=[{
            "module_name": "tests.model_manager_test",
            "class_name": "MLModelMock"
        }])

        # act
        exception_raised = False
        model_object = None
        # accessing the MLModelMock model object
        try:
            model_object = model_manager.get_model(qualified_name="qualified_name")
        except Exception as e:
            exception_raised = True
            print_tb(e)

        # assert
        self.assertFalse(exception_raised)
        self.assertTrue(model_object is not None)

    def test2(self):
        """testing that the ModelManager will return the same instance of an MLModel class from several different
        instances of ModelManager"""
        # arrange
        # instantiating the model manager class
        first_model_manager = ModelManager()

        # loading the MLModel objects from configuration
        first_model_manager.load_models(configuration=[
            {
                "module_name": "tests.model_manager_test",
                "class_name": "MLModelMock"
            }
        ])

        # act
        first_model_object = first_model_manager.get_model(qualified_name="iris_model")

        # instantiating the ModelManager class again
        second_model_manager = ModelManager()

        second_model_object = second_model_manager.get_model(qualified_name="iris_model")

        # assert
        self.assertTrue(str(first_model_object) == str(second_model_object))

    def test3(self):
        """ testing that the ModelManager only allows MLModel objects to be stored """
        # arrange
        model_manager = ModelManager()

        # act
        exception_raised = False
        exception_message = ""
        try:
            model_manager.load_models(configuration=[
                {
                    "module_name": "tests.model_manager_test",
                    "class_name": "SomeClass"               # using the class defined at the top of this file to test
                }
            ])
        except Exception as e:
            exception_raised = True
            exception_message = str(e)

        # assert
        self.assertTrue(exception_raised)
        self.assertTrue(exception_message == "The ModelManager can only hold references to objects of type MLModel.")

    def test4(self):
        """ testing that the ModelManager returns None when a model is not found """
        # arrange
        model_manager = ModelManager()
        model_manager.load_models(configuration=[
            {
                "module_name": "tests.model_manager_test",
                "class_name": "MLModelMock"
            }
        ])

        # act
        exception_raised = False
        exception_message = ""
        try:
            model = model_manager.get_model(qualified_name="asdf")
        except Exception as e:
            exception_raised = True
            exception_message = str(e)

        # assert
        self.assertFalse(exception_raised)
        self.assertTrue(model is None)


if __name__ == '__main__':
    unittest.main()