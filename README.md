## Concept:
A particular kind of neural network architecture known as a "teacher-student 
network" includes teaching a smaller, simpler network (the student) to replicate 
the behaviour of a more complicated, larger network (the teacher). Although the 
student network is trained on the same task as the teacher network, it is trained 
to learn from the intermediate representations of the teacher network, which are 
used as "hints" or "soft targets," rather than directly attempting to minimise the 
prediction error. This process is called knowledge distillation.<br>
The following are some advantages of using a teacher-student network:
 Training becomes faster and more effective when the student network 
learns from the intermediate representations of the teacher network rather 
than starting from scratch.<br>
 Improved generalisation: By minimising overfitting and enhancing the 
generalisation capabilities of the student network, the instructor network 
can provide a regularisation impact.<br>
 Model compression: The student network is often simpler and smaller than 
the teacher network, which increases its computational efficiency and 
makes it simpler to implement in contexts with limited resources. <br>
## Choice of Hyperparameters
I used the following hyperparameters for training the teacher model: <br>
**optimizer = optim.Adam(teacher_net.parameters(), lr=0.001)**
<br>
Faster convergence: Adam's adjustable learning rate can result in faster 
convergence and improved optimisation performance, especially 
Robustness: robustness to the selection of hyperparameters like learning rate.
Reduced memory requirements: Adam is more memory-efficient for largescale issues, as it does not require the recording of the whole gradient history 
for each parameter. <br>
**criterion = nn.CrossEntropyLoss()**
<br>
It works well for classification issues: For classification issues with 
numerous classes, cross entropy loss works very effectively. It severely 
penalises the model for giving the wrong classes high probability while 
rewarding it for giving the right class high probability.
It is distinct and simple to optimise: Since the cross entropy loss function is 
differentiable with respect to the predicted probabilities, gradient descent 
or other gradient-based optimisation methods can be used to optimise it. <br>
**batch size= 1024&epochs= 5:**
<br>
I have chosen a larger batch for a faster training, as the tiny 
ImageNet dataset has over 100,000 images, so it takes a lot of 
time to train
Previously I used the batch size= 100, but it was taking too long to 
train
