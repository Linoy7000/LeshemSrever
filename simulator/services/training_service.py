import logging
import traceback

import numpy as np
from sklearn.linear_model import LinearRegression
from simulator.models import TrainingData, Element


class Training:

    def __init__(self, design, elements):

        # Retrieve only the relevant data by product
        training_data = TrainingData.objects.order_by('id').filter(product__id=design)

        # Get values of container\element dimensions, position for the elements
        container_width = np.array(training_data.values_list('container_width', flat=True))
        container_height = np.array(training_data.values_list('container_height', flat=True))
        element_id = np.array(training_data.values_list('element', flat=True))
        position_x = np.array(training_data.values_list('position_x', flat=True))
        position_y = np.array(training_data.values_list('position_y', flat=True))
        width = np.array(training_data.values_list('width', flat=True))
        height = np.array(training_data.values_list('height', flat=True))

        self.unique_element_values = np.unique(element_id)

        # Store alternative elements for excluded elements
        self.excluded_elements = {}

        for element in elements:

            excluded_element = self.is_excluded(element)

            if excluded_element:
                # Get element type
                type_id = Element.objects.get(id=excluded_element).type.id
                # Get data of similar elements
                training_data = training_data.filter(element__type__id=type_id)
                alternative_element = training_data[0].element.id
                # Append to the existing data
                container_width = np.append(container_width, np.array(training_data.values_list('container_width', flat=True)))
                container_height = np.append(container_height, np.array(training_data.values_list('container_height', flat=True)))
                element_id = np.append(element_id, np.array(training_data.values_list('element', flat=True)))
                position_x = np.append(position_x, np.array(training_data.values_list('position_x', flat=True)))
                position_y = np.append(position_y, np.array(training_data.values_list('position_y', flat=True)))
                width = np.append(width, np.array(training_data.values_list('width', flat=True)))
                height = np.append(height, np.array(training_data.values_list('height', flat=True)))

                self.unique_element_values = np.append(self.unique_element_values, alternative_element)

                self.excluded_elements[excluded_element] = alternative_element

        # >>> Width <<< #
        # Independent Variables
        X_width = np.column_stack((container_width, element_id))
        # Dependent Variables
        Y_width = np.column_stack((position_x, width))

        # >>> Height <<< #
        # Independent Variables
        X_height = np.column_stack((container_height, element_id))
        # Dependent Variables
        Y_height = np.column_stack((position_y, height))

        self.models_width = {value: None for value in self.unique_element_values.tolist()}
        self.models_height = {value: None for value in self.unique_element_values.tolist()}

        self.prepare_models(element_id, X_width, Y_width, X_height, Y_height)

    def prepare_models(self, element_id, X_width, Y_width, X_height, Y_height):
        """ Prepare models for prediction """
        for value in self.unique_element_values:
            try:
                # Create filter mask
                indices = np.where(element_id == value)

                # >>> Width <<< #
                # Get values that refer to the current element
                X_width_subset = X_width[indices]
                Y_width_subset = Y_width[indices]
                # Train model
                model_width = LinearRegression()
                model_width.fit(X_width_subset, Y_width_subset)
                # Store model
                self.models_width[value] = model_width

                # >>> Height <<< #
                # Get values that refer to the current element
                X_height_subset = X_height[indices]
                Y_height_subset = Y_height[indices]
                # Train model
                model_height = LinearRegression()
                model_height.fit(X_height_subset, Y_height_subset)
                # Store model
                self.models_height[value] = model_height

            except Exception as e:
                raise Exception(e)

    def predict(self, width, height, element_id):

        if element_id in self.excluded_elements.keys():
            element_id = self.excluded_elements[element_id]

        try:
            # Get the stored model
            model_width = self.models_width[element_id]
            model_height = self.models_height[element_id]

            if model_width and model_height:
                # Values to predict
                width = np.array([[width, element_id]])
                height = np.array([[height, element_id]])
                # Predict
                width_predict = model_width.predict(width)[0]
                height_predict = model_height.predict(height)[0]
                return width_predict, height_predict
            else:
                raise ValueError(f"No model found for type: {element_id}")
        except KeyError as e:
            raise Exception(e)

    def is_excluded(self, element):
        if element not in self.unique_element_values:
            return element
        return None
        
