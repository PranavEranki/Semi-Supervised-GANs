# Semi- Supervised GANs for Data Efficient Classification - Weekly Updates

**Auhor:** Pranav Eranki

**Project Description:** I am working on using GANs to generate images of tissues and cells. Then, I wish to leverage the learned representations and extend the discriminator to classify the tissue as cancerous and non-cancerous.

## Weekly Updates

### Oct 24, 2018 - Oct 31, 2018(10/24 - 10/31)
Complete? | Tasks
------ | ---------------
Yes | Tuning hyperparameters of the SGAN and working on different loss functions / optimizations techniques to achieve good performance on the cancer dataset.
Yes |  Working on discriminator training in the SGAN architecture that improves classification accuracy using fewer annotated samples.
Yes | Creating the annotated dataset using the bitmaps (given from PathAI) that denote the tissue region to remove empty patches from the tissue slide.

### Oct 10, 2018 - Oct 17, 2018(10/10 - 10/17)
Complete? | Tasks
------ | ---------------
Yes | Training and tuning hyperparameters of the SGAN to obtain optimial performance over the dataset.
Yes | Running SGAN with ConvTranspose operation over Upsampling to improve performance. Working on identifying factors that will affect the current SGAN architecture when employed on the actual cancer dataset.
Yes | Work to create patches and their annotation to train the SGAN on the new curated dataset of cancer images.


### Oct 3, 2018 - Oct 10, 2018(10/03 - 10/10)
Complete? | Tasks
------ | ---------------
Yes | Tune the percentage of supervised and unsupervised samples in the training phase and try to decrease this with optimal performance. Also, look at complement generator to improve the accuracy of semi-supervised classification on MNIST.
Yes | Experiment with different generator and discriminator architectures to improve the training of the Semi Supervised GANs. Also, examine the usage of Deconvolution layers over Upsampling in the SGAN architecture to improve performance.
Yes | Incorporate new slide images from the LUSC and SKCM cancerous groups into the image-patching framework. Also, train the SGAN on the newly curated dataset of high resolution cancer images.

### Sep 26, 2018 - Oct 3, 2018 (09/26 - 10/03)
Complete? | Tasks
------ | ---------------
Yes | I need to work to obtain the accuracy of real and fake generated images and the accuracy of the classification of images on MNIST data with the Semi-supervised GAN. Also obtain metric to get the percentage of supervised samples being used to train and try to decrease this with optimal performance.
Yes | Explore different architectures that improve the training of the Semi Supervised GANs. Implement improved GAN training techniques such as minibatch discrimination on the existing SGAN.
Yes | Obtain the dataset from the CAMELYON 2017 dataset. Implement the framework to get patch level label annotation from the lesion level label annotation.


### Sep 19, 2018 - Sep 26, 2018 (09/19 - 09/26)
Complete? | Tasks
------ | ---------------
 Yes | Implement a semi-supervised GAN on the MNIST Dataset and explore Least squares GAN for as a way of stabilizing the GAN training.
 Yes | Explore different methods to improve training of GANs on the standard DCGAN such as Mini-batch discrimination and virtual batch normalization.
 Yes | Improve the performance of the DCGAN by implementing techniques such as historical averaging and one-sided label smoothing to improve GAN training.


### Sep 12, 2018 - Sep 19, 2018 (09/12 - 09/19)
Complete? | Tasks
------ | ---------------
Yes | Explore how condiational GANs can be leveraged for problem statement. Implement a simple CycleGAN in PyTorch on the dataset being used in the CycleGAN paper (maps dataset).
Yes | Perform literature survey on the various applications of semi-supervised GANs. Implement a Vanilla GAN and get it running on the MNIST dataset. Evaluate the performance of the GAN and implement different distance metrics on the GAN.
Yes | Go through the approaches mentioned in the Camelyon17 Challenge and their basic implementations. Implement DCGAN and evalute performance on MNIST Dataset.


### Sep 5, 2018 - Sep 12, 2018 (09/05 - 09/12)

Complete? | Tasks
------ | ---------------
Yes | Read papers on the variants of GANs in order to understand their implementation details. Further performed literature survey on state of the art on semi-supervised learning with GANs and CycleGANs.
Yes | Did a literature survey on exisitng techniques used for tissue classification. Analyzed and identified various distance metrics that can be used between the generated and trained probability distributions for the task. Performed literature survey on GAN architectures and improved techniques for training GANs
Yes | Explored publicly available annotated datasets for the project (<https://cancergenome.nih.gov/>). Performed literature survey on DCGANS, state of the art on semi-supervised learning with GANs and work on Progressive growing of GANs to generate high resolution images.
