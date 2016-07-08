package utilities;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileWriter;
import java.io.IOException;
import java.util.Collection;
import java.util.List;
import java.util.logging.Level;
import java.util.logging.Logger;
import java.util.regex.Pattern;

import model.Database;

import org.deeplearning4j.models.embeddings.loader.WordVectorSerializer;
import org.deeplearning4j.models.embeddings.wordvectors.WordVectors;
import org.deeplearning4j.models.word2vec.Word2Vec;
import org.deeplearning4j.text.sentenceiterator.FileSentenceIterator;
import org.deeplearning4j.text.sentenceiterator.SentenceIterator;
import org.deeplearning4j.text.tokenization.tokenizerfactory.DefaultTokenizerFactory;
import org.deeplearning4j.text.tokenization.tokenizerfactory.TokenizerFactory;
import org.deeplearning4j.util.SerializationUtils;
import org.jsoup.Jsoup;
import org.nd4j.linalg.factory.Nd4j;

/**
 *
 * @author amendrashrestha
 */
public class IOReadWrite {

//    private static final Pattern UNDESIRABLES = Pattern.compile("[★(),.;!-?<>%\\*]");
    private static final Pattern UNDESIRABLES = Pattern.compile("[,.?★*;\\]\\[\\(\\)]");

    public static String FilterPost(String text) {
        text = text.toLowerCase();
        text = Jsoup.parse(text).text();
        text = UNDESIRABLES.matcher(text).replaceAll(" ") + " ";
        return text;
    }

    public static void DrugPosts() {
        String tableName = "tbl_drugs_info_new";

        List<String> posts = Database.getPost(tableName);

        for (String post : posts) {
            try {
                String filtered_posts = FilterPost(post);
                writeIntoFile(filtered_posts);
            } catch (IOException ex) {
                Logger.getLogger(IOReadWrite.class.getName()).log(Level.SEVERE, null, ex);
            }
        }
    }

    private static void writeIntoFile(String filtered_posts) throws IOException {
        try (FileWriter fw = new FileWriter(IOProperties.DRUG_TEXT_FILEPATH, true)) {
            fw.write(filtered_posts + "\n");
        }
    }

    public static void Word2VecModel() throws IOException {

        main.main.log.info("Load & Vectorize Sentences....");
        File file = new File(IOProperties.DRUG_TEXT_FILEPATH);
        SentenceIterator iter = new FileSentenceIterator(file);

        TokenizerFactory t = new DefaultTokenizerFactory();

        int layerSize = 300;

        Word2Vec vec = new Word2Vec.Builder().sampling(1e-5).
                minWordFrequency(5).batchSize(1000).useAdaGrad(false).
                layerSize(layerSize).iterations(3).learningRate(0.025).
                minLearningRate(1e-2).negativeSample(10).iterate(iter).
                tokenizerFactory(t).build();
        vec.fit();

        Nd4j.ENFORCE_NUMERICAL_STABILITY = true;

//        main.main.log.info("Writing word vectors to text file....");
        SerializationUtils.saveObject(vec, new File(IOProperties.MODEL_FILEPATH + "w2v_model.ser"));
        WordVectorSerializer.writeWordVectors(vec, IOProperties.MODEL_FILEPATH + "w2v_vectors.txt");
    }

    public static void TestModel() {

        try {
            WordVectors wordVectors = WordVectorSerializer.
                    loadTxtVectors(new File(IOProperties.MODEL_FILEPATH + "w2v_vectors.txt"));

            String word1 = "cocaine";
            String word2 = "money";

            double sim = wordVectors.similarity(word1, word2);
            System.out.println("Similarity between " + word1 + " and " + word2 + " : " + sim);

//            main.main.log.info("Closest Words:");
            Collection<String> similar = wordVectors.wordsNearest(word1, 20);
            System.out.println("word similar with " + word1 + " --> " + similar);
        } catch (FileNotFoundException ex) {
            Logger.getLogger(IOReadWrite.class.getName()).log(Level.SEVERE, null, ex);
        }
    }

}
