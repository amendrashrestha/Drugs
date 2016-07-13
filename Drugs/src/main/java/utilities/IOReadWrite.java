package utilities;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileWriter;
import java.io.IOException;
import java.util.Collection;
import java.util.List;
import java.util.logging.Level;
import java.util.logging.Logger;
import java.util.regex.Matcher;
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
    private static final Pattern UNDESIRABLES = Pattern.compile("[!,.?★*;\\]\\[\\(\\)\"-]");

    public static String filterPost(String text) {
        text = text.toLowerCase();
        text = UNDESIRABLES.matcher(text).replaceAll(" ") + " ";
        return text;
    }

    private static String removeDate(String post_remove_html) {
        String date = "[a-zA-Z]+ [0-9]{2}, [0-9]{4}, ([01]?[0-9]|2[0-3]):[0-5][0-9]:[0-5][0-9] [a-z]{2}";
        Pattern hPattern = Pattern.compile(date);
        Matcher m = hPattern.matcher(post_remove_html);

        while (m.find()) {
            post_remove_html = post_remove_html.replaceAll(date, "");
        }
        return post_remove_html;
    }

    public static String removeHTML(String text) {
        text = Jsoup.parse(text).text();
        String urlPattern = "((https?|ftp|gopher|telnet|file|Unsure|http):((//)|"
                + "(\\\\))+[\\w\\d:#@%/;$()~_?\\+-=\\\\\\.&]*)";
        Pattern uPattern = Pattern.compile(urlPattern, Pattern.CASE_INSENSITIVE);
        Matcher m = uPattern.matcher(text);

        while (m.find()) {
            String urlStr = m.group();
            text = text.replaceAll(Pattern.quote(urlStr), "").trim();
        }
        return text;
    }

    public static void DrugPosts(String filepath) {
        String tableName = "tbl_drugs_info_new";

        List<String> posts = Database.getPost(tableName);

        for (String post : posts) {
            try {
                String post_remove_html = removeHTML(post);
                String post_remove_date = removeDate(post_remove_html);
                String filtered_posts = filterPost(post_remove_date);

                writeIntoFile(filtered_posts, filepath);
            } catch (IOException ex) {
                Logger.getLogger(IOReadWrite.class.getName()).log(Level.SEVERE, null, ex);
            }
        }
    }

    public static void AlternativeMediaPosts(String filepath) {
        String[] newsType = new String[]{"nordfront", "avpixlat", "exponerat",
            "fritider", "nyheteridag", "samtiden", "aftonbladet", "DN"};
        String tableName = "tbl_news_";

        for (String single_newsType : newsType) {
            System.out.println("*********** " + single_newsType + " ***********");
            List<String> posts = Database.getAltMediaPost(tableName + single_newsType);

            for (String post : posts) {
                try {
                    String post_remove_html = removeHTML(post);
                    String post_remove_date = removeDate(post_remove_html);
                    String filtered_posts = filterPost(post_remove_date);

                    writeIntoFile(filtered_posts, filepath);
                } catch (IOException ex) {
                    Logger.getLogger(IOReadWrite.class.getName()).log(Level.SEVERE, null, ex);
                }
            }
        }
    }

    private static void writeIntoFile(String filtered_posts, String filepath) throws IOException {
        try (FileWriter fw = new FileWriter(filepath, true)) {
            fw.write(filtered_posts + "\n");
        }
    }

    public static void Word2VecModel(String filepath, String modelFilePath) throws IOException {

        main.main.log.info("Load & Vectorize Sentences....");
        File file = new File(filepath);
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
//        SerializationUtils.saveObject(vec, new File(IOProperties.MODEL_FILEPATH + "w2v_model.ser"));
        WordVectorSerializer.writeWordVectors(vec, modelFilePath + "w2v_vectors.txt");
    }

    public static void TestModel(String modelFilepath) {

        try {
            WordVectors wordVectors = WordVectorSerializer.
                    loadTxtVectors(new File(modelFilepath + "w2v_vectors.txt"));

            String word1 = "grass";
            String word2 = "weed";

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
