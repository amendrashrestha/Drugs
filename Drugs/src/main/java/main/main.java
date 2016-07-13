package main;

import java.io.File;
import java.io.IOException;
import java.util.logging.Level;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import utilities.IOProperties;
import utilities.IOReadWrite;

/**
 *
 * @author amendrashrestha
 */
public class main {

    public static Logger log = LoggerFactory.getLogger(main.class);

    static void initDrug() throws IOException {
        File liwcCountFile = new File(IOProperties.DRUG_TEXT_FILEPATH);

        if (!liwcCountFile.exists()) {
            IOReadWrite.DrugPosts(IOProperties.DRUG_TEXT_FILEPATH);
            IOReadWrite.Word2VecModel(IOProperties.DRUG_TEXT_FILEPATH, IOProperties.DRUG_MODEL_FILEPATH);
        }
        System.out.println("Testing model......");
        IOReadWrite.TestModel(IOProperties.DRUG_MODEL_FILEPATH);
    }

    public static void main(String[] args) throws IOException {
//        initDrug();
        initAlternativeMedia();
    }

    private static void initAlternativeMedia() {

        File liwcCountFile = new File(IOProperties.ALT_MEDIA_TEXT_FILEPATH);

        if (!liwcCountFile.exists()) {
            IOReadWrite.AlternativeMediaPosts(IOProperties.ALT_MEDIA_TEXT_FILEPATH);
        }
        System.out.println("Testing model......");
        IOReadWrite.TestModel(IOProperties.ALT_MEDIA_MODEL_FILEPATH);
    }

}
