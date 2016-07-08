package main;

import java.io.File;
import java.io.IOException;

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

    static void init() throws IOException {
        File liwcCountFile = new File(IOProperties.DRUG_TEXT_FILEPATH);

//        if (!liwcCountFile.exists()) {
//            IOReadWrite.DrugPosts();
            IOReadWrite.Word2VecModel();
//        }
        System.out.println("Testing model......");
        IOReadWrite.TestModel();
    }

    public static void main(String[] args) throws IOException {
        init();
    }

}
