# 2+1 wave plotting

## Quick links
**_TUTUORIAL_**: [HOW TO RUN THE 2+1 WAVE VISUALISATION PROJECT]()

**_TO TEST THE CODE, ACCESS THIS_**: [GOOGLE COLAB CODE](https://colab.research.google.com/drive/1QVAfFcDTj8onUciqTtq9gnGhLE3H-X_j?usp=sharing)

# Documentation

## Table of Contents
- [1) Introduction](#1-introduction)
  - [Why Google Colab?](#why-google-colab)
  - [Project overview](#project-overview) 
  - [Objectives and purpose](#objectives-and-purpose) 
- [2) In-depth view analysis](#2-in-depth-view-analysis)
  - [Waveforms explanation](#waveforms-explanation)
  - [Mathematical basis](#mathematical-basis)
- [3) Implementation](#3-implementation)
  - [Tools and libraries used](#tools-and-libraries-used)
  - [Code explanation](#code-explanation)
- [4) How to use the project](#4-how-to-use-the-project)
- [5) Future improvements](#5-future-improvements)
- [6) Conclusion](#6-conclusion)

## 1) Introduction
The project is written in Python. But it’s running in a Google Colab.

### Why Google Colab?
Google Colab (short for Colaboratory) is a cloud-based platform provided by Google that allows users to write, execute, and share Python code in a web-based environment. It is particularly well-suited for tasks involving data analysis, machine learning, and scientific computing, as it provides free access to computational resources such as GPUs and TPUs.

Google Colab eliminates the need for extensive local setup by enabling code execution directly in the cloud. This means that users do not need to install Python or additional libraries on their local machines, as all dependencies can be specified and installed within the Colab notebook. Furthermore, Colab notebooks are easily shareable via links, making collaboration and distribution of code straightforward.

In the context of this project, I chose Google Colab because it ensures that my wave plotting code can be accessed and run seamlessly anywhere, anytime by anyone, without requiring any configuration of the project on local machines. By hosting the code on Colab, I can provide a ready-to-run environment where the project can be executed interactively, enhancing both accessibility and user experience.

### Project overview

### Objectives and purpose


## 2) In-depth view analysis

### Waveforms explanation

The fundamental wave equation for 2+1 dimension is: 
$\phi \square=0$

$\square = -\frac{\partial^2}{\partial t^2} + \nabla ^ 2$

where $\nabla$ is the 

$\frac{\partial^2\phi}{\partial t^2}=c^2(\frac{\partial^2\phi}{\partial x^2}+\frac{\partial^2\phi}{\partial y^2})$

where: 
- $\phi(x, y, t)$ is the wave amplitude
- $c$ is the wave speed
- $x$ and $y$ are the space coordinates 
- $t$ is the time coordinates
- $\square$ is the d'Alembertian operator

Which can also be written as: 

Where $\square$ is also known as d'Alambert operator and is equal to: <br>
$\square = -\frac{1}{c^2}  \frac{\partial^2}{\partial t^2} + \frac{\partial^2}{\partial x^2}+\frac{\partial^2}{\partial y^2}$


### Mathematical basis


## 3) Implementation

### Tools and libraries used

The wave amplitude $\phi(x, y, t)$ is stored in a 3D array, known in the code as ```phi```: 
- $\phi[:, :, 0]:t - \triangle t$ is the previous timestep 
- $\phi[:, :, 0]:t$ is the current timestep
- $\phi[:, :, 0]:t + \triangle t$ is the next timestep 

The Laplacian is calculated using central finite differences. 

The wave starts as a Gaussian Pulse centred in ```(x_start, y_start)``` with a specified width. 

### Runge-Kutta for time integration

For time integration, we can switch to Runge-Kutta (RK4) for time evolution. It means replacing the finite difference time integration with the RK4 scheme: 

1. We compute:
   - $k_1=S(t^n, \phi^n)$
   - $k_2=S(t^n + \frac{\triangle t}{2}, \phi^n + \frac{\triangle t}{2}k_1)$
   - $k_3=S(t^n + \frac{\triangle t}{2}, \phi^n + \frac{\triangle t}{2}k_2)$
   - $k_4=S(t^n + \triangle t, \phi^n + \triangle t k_3)$
2. We update $\phi^{n+1} = \phi^n + \frac{\triangle t}{6}(k_1 + 2k_2 + 2k_3 + k_4)$

### Code explanation
This section provides a detailed breakdown of the code used in the project. 

#### 0) Installing all of the required libraries

#### 1) Importing required libraries 
The first step is to import the necessary libraries for this project. These libraries provide tools for numerical computation and visualization. 

```python 

```

- **NumPy** - used for efficient numerical operations such as generating arrays and performing mathematical functions 
- **Matplotlib** - used for creating static, animated and interactive plots

#### 2) Defining the parameters
The parameters of the wave are defined to allow customization and flexibility.

### Plots examples


## 4) How to use the project

## 5) Future improvements

## 6) Conclusion


