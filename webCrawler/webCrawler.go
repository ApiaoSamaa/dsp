package main

import (
	"encoding/csv"
	"encoding/json"
	"fmt"
	"io"
	"log"
	"net/http"
	"os"
	"strings"
	"sync"

	//"strings"
	"net/http/cookiejar"
	"net/url"
	"path"
	"path/filepath"
	"time"

	"github.com/PuerkitoBio/goquery"
)

func getDiseaseidFromTSV(filename string) ([]string, error) {
	var firstColumn []string
	file, err := os.Open(filename)
	if err != nil {
		return nil, err
	}
	defer file.Close()

	r := csv.NewReader(file)
	r.Comma = '\t'
	for {
		record, err := r.Read()
		if err == io.EOF {
			break
		}
		if err != nil {
			return nil, err
		}
		firstColumn = append(firstColumn, record[0])
	}
	return firstColumn, err
}

func fetchGeneLinks(client *http.Client, term string) ([]string, error) {
	url := fmt.Sprintf("https://www.ncbi.nlm.nih.gov/clinvar/?term=%s", term)
	resp, err := client.Get(url)
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()

	doc, err := goquery.NewDocumentFromReader(resp.Body)
	if err != nil {
		return nil, err
	}

	var geneLinks []string
	doc.Find("a").Each(func(i int, s *goquery.Selection) {
		href, exists := s.Attr("href")
		if exists && strings.HasPrefix(href, "/gene/") {
			finalLink := "https://www.ncbi.nlm.nih.gov" + href
			geneLinks = append(geneLinks, finalLink)
		}
	})

	return geneLinks, nil
}

func downloadGeneData(client *http.Client, geneLink string, outputDir string) error {

	// FIND LINK TO DOWNLOAD DATA
	var url = ""
	fileName := path.Base(url)
	outputPath := filepath.Join(outputDir, fileName)

	resp, err := client.Get(geneLink)
	if err != nil {
		return err
	}
	defer resp.Body.Close()

	// Create the file in the specified directory
	outFile, err := os.Create(outputPath)
	if err != nil {
		return err
	}
	defer outFile.Close()

	// Copy the contents of the HTTP response body to the file
	_, err = io.Copy(outFile, resp.Body)
	if err != nil {
		return err
	}

	return nil
}

type Cookie struct {
	Domain         string  `json:"domain"`
	ExpirationDate float64 `json:"expirationDate,omitempty"`
	Name           string  `json:"name"`
	Value          string  `json:"value"`
	Path           string  `json:"path"`
	Secure         bool    `json:"secure"`
	HttpOnly       bool    `json:"httpOnly"`
}

func main() {
	terms, err := getDiseaseidFromTSV("disease_associations.tsv")
	if err != nil {
		log.Fatal(err)
	}

	myCookiePath := "myCookie.json"
	myCookie, err := os.ReadFile(myCookiePath)
	if err != nil {
		log.Fatal("Failed to read file: %v", err)
	}
	var cookies []Cookie
	err = json.Unmarshal(myCookie, &cookies)
	if err != nil {
		log.Fatalf("Failed to unmarshal JSON: %v", err)
	}

	jar, _ := cookiejar.New(nil)

	for _, cookieData := range cookies {
		cookie := &http.Cookie{
			Name:     cookieData.Name,
			Value:    cookieData.Value,
			Path:     cookieData.Path,
			Domain:   cookieData.Domain,
			Secure:   cookieData.Secure,
			HttpOnly: cookieData.HttpOnly,
		}
		if cookieData.ExpirationDate != 0 {
			cookie.Expires = expirationTime(cookieData.ExpirationDate)
		}
		u, err := url.Parse("https://" + cookieData.Domain)
		if err != nil {
			log.Fatalf("Failed to parse URL: %v", err)
		}
		jar.SetCookies(u, []*http.Cookie{cookie})
	}
	client := &http.Client{
		Jar: jar,
	}

	var wg sync.WaitGroup
	outputDir := "/Users/a123/proj/genePaper/dsp/DData"

	for _, term := range terms {
		wg.Add(1)
		// go func(term string) {
		defer wg.Done()
		searchURL := fmt.Sprintf("https://www.ncbi.nlm.nih.gov/clinvar/?term=%s", term)
		geneLinks, err := fetchGeneLinks(client, searchURL)
		if err != nil {
			log.Printf("Failed to get gene links for term %s: %v", term, err)
			return
		}

		for _, geneLink := range geneLinks {
			err := downloadGeneData(client, geneLink, outputDir)
			if err != nil {
				log.Printf("Failed to download data for link %s: %v", geneLink, err)
				continue
			}
			fmt.Println("Downloaded data from:", geneLink)
			// Add delay to respect the website's terms and not overwhelm their servers
			time.Sleep(2 * time.Second)
		}
		// }(term) // HERE ESPECIALLY IMPORTANT
	}
	wg.Wait()
}
func expirationTime(unixTime float64) time.Time {
	return time.Unix(int64(unixTime), 0)
}
