

## Menu

* [Simulator](#Simulator)
  - [Key Features](#Key-Features)
  - [How It Works](#How-It-Works)
  - [File Structure](#File-Structure)
  - [3D Visualization](#3D-Visualization)
  
* Marketing Site Api
  
  - [Products](#Products)
  - [Orders](#Orders)
  - [Contacts](#Contacts)


## **Simulator**

This module enables dynamic product simulation by integrating specific elements into the design. The size and positioning of these elements are dynamically adjusted based on user preferences, product dimensions, and insights derived from trained data. This approach ensures a highly customized and data-driven simulation experience.

### **Key Features**
_Customizable Elements:_ Allows users to select elements to include in the product simulation.

_Dynamic Sizing and Positioning:_ Adjusts the size and position of elements based on product dimensions and user input.

_Data-Driven Simulation:_ Uses existing data to calculate optimal configurations for elements within the product.

### **How It Works**
User Selection: Users specify the elements they want to include in the product.

Dimension Calculation: The system calculates element sizes and positions based on product dimensions and existing data.

Simulation Output: A visual representation of the product is generated, showcasing the integrated elements.

### **File Structure**
[training_service.py](simulator%2Fservices%2Ftraining_service.py)
[simulator_service.py](simulator%2Fservices%2Fsimulator_service.py)

### **3D Visualization**
calculates and renders a 3D representation of a product using CSS on the client side, providing a dynamic and realistic visualization.
[perspective_service.py](simulator%2Fservices%2Fperspective_service.py)

## API


### **Products**
    

- _Get Products List_
   
        GET products/

- _Get Specific Product_
    
      GET products/{id}

- _Create Product_
   
      POST products/

- _Update Product_
    
        PUT products/{id}

- _Partial Update_
   
        PATCH products/{id}



### **Orders**

- _Get Orders List_
   
        GET orders/

- _Get Specific Order_
    
        GET orders/{id}

- _Create Order_
   
        POST orders/

- _Update Order_
    
        PUT orders/{id}

- _Partial Update_
   
        PATCH orders/{id}

### **Contacts**

- _Get Contacts List_
   
        GET contacts/

- _Get Specific Contact_
    
        GET contacts/{id}

- _Create Contact_
   
        POST contacts/

- _Update Contact_
    
        PUT contacts/{id}

- _Partial Update_
   
        PATCH contacts/{id}

