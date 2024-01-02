# BeReal Date Tagger

Have you ever wanted to export your BeReals only to find out the images aren't sorted correctly by date?

Well I have. So I wrote this script to do the work for me

## Prerequisites

You need to request a copy of your data from BeReal. The images themselves don't contain the metadata however it is located in the json files that come along with it.

Make sure that the copy of your data has been unzipped

## Installation

```
python -m pip install -r requirements.txt -U
```

## Usage

```
python main.py -i <input_directory> -o <output_directory> [-t <timezone>}
```

Timezone name must be among the `pytz`'s supported names. Your safest bet though is using the `<Region/City>` format. See example below.

### A quick warning

* All images will be tagged using the same timezone. If no timezone is provided, UTC time will be used.

* Directories provided when running the program is relative to the location of the main.py file.

### Example

```
python main.py -i ../my-unzipped-bereal-data -o ../tagged-bereal-images -t Asia/Seoul
```
