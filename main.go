package main

import (
	"encoding/csv"
	"encoding/json"
	"fmt"
	"os"
	"strings"
	"sync"
	"time"

	"github.com/gocolly/colly/v2"
)

type StaffMember struct {
	Name       string `json:"name"`
	Title      string `json:"title"`
	Department string `json:"department"`
	Email      string `json:"email"`
	Phone      string `json:"phone"`
	Location   string `json:"location"`
	Position   string `json:"position"`
	ProfileURL string `json:"profile_url"`
}

// 简单的HTML实体解码函数
func decodeHTMLEntities(s string) string {
	// 解码常见的HTML实体 - 扩展版本
	s = strings.ReplaceAll(s, "&#x61;", "a")
	s = strings.ReplaceAll(s, "&#x62;", "b")
	s = strings.ReplaceAll(s, "&#x63;", "c")
	s = strings.ReplaceAll(s, "&#x64;", "d")
	s = strings.ReplaceAll(s, "&#x65;", "e")
	s = strings.ReplaceAll(s, "&#x66;", "f")
	s = strings.ReplaceAll(s, "&#x67;", "g")
	s = strings.ReplaceAll(s, "&#x68;", "h")
	s = strings.ReplaceAll(s, "&#x69;", "i")
	s = strings.ReplaceAll(s, "&#x6A;", "j")
	s = strings.ReplaceAll(s, "&#x6B;", "k")
	s = strings.ReplaceAll(s, "&#x6C;", "l")
	s = strings.ReplaceAll(s, "&#x6D;", "m")
	s = strings.ReplaceAll(s, "&#x6E;", "n")
	s = strings.ReplaceAll(s, "&#x6F;", "o")
	s = strings.ReplaceAll(s, "&#x70;", "p")
	s = strings.ReplaceAll(s, "&#x71;", "q")
	s = strings.ReplaceAll(s, "&#x72;", "r")
	s = strings.ReplaceAll(s, "&#x73;", "s")
	s = strings.ReplaceAll(s, "&#x74;", "t")
	s = strings.ReplaceAll(s, "&#x75;", "u")
	s = strings.ReplaceAll(s, "&#x76;", "v")
	s = strings.ReplaceAll(s, "&#x77;", "w")
	s = strings.ReplaceAll(s, "&#x78;", "x")
	s = strings.ReplaceAll(s, "&#x79;", "y")
	s = strings.ReplaceAll(s, "&#x7A;", "z")
	s = strings.ReplaceAll(s, "&#x40;", "@")
	s = strings.ReplaceAll(s, "&#x2E;", ".")
	s = strings.ReplaceAll(s, "&#x2D;", "-")
	s = strings.ReplaceAll(s, "&#x5F;", "_")

	// 解码十进制HTML实体
	s = strings.ReplaceAll(s, "&#97;", "a")
	s = strings.ReplaceAll(s, "&#98;", "b")
	s = strings.ReplaceAll(s, "&#99;", "c")
	s = strings.ReplaceAll(s, "&#100;", "d")
	s = strings.ReplaceAll(s, "&#101;", "e")
	s = strings.ReplaceAll(s, "&#102;", "f")
	s = strings.ReplaceAll(s, "&#103;", "g")
	s = strings.ReplaceAll(s, "&#104;", "h")
	s = strings.ReplaceAll(s, "&#105;", "i")
	s = strings.ReplaceAll(s, "&#106;", "j")
	s = strings.ReplaceAll(s, "&#107;", "k")
	s = strings.ReplaceAll(s, "&#108;", "l")
	s = strings.ReplaceAll(s, "&#109;", "m")
	s = strings.ReplaceAll(s, "&#110;", "n")
	s = strings.ReplaceAll(s, "&#111;", "o")
	s = strings.ReplaceAll(s, "&#112;", "p")
	s = strings.ReplaceAll(s, "&#113;", "q")
	s = strings.ReplaceAll(s, "&#114;", "r")
	s = strings.ReplaceAll(s, "&#115;", "s")
	s = strings.ReplaceAll(s, "&#116;", "t")
	s = strings.ReplaceAll(s, "&#117;", "u")
	s = strings.ReplaceAll(s, "&#118;", "v")
	s = strings.ReplaceAll(s, "&#119;", "w")
	s = strings.ReplaceAll(s, "&#120;", "x")
	s = strings.ReplaceAll(s, "&#121;", "y")
	s = strings.ReplaceAll(s, "&#122;", "z")
	s = strings.ReplaceAll(s, "&#64;", "@")
	s = strings.ReplaceAll(s, "&#46;", ".")
	s = strings.ReplaceAll(s, "&#45;", "-")
	s = strings.ReplaceAll(s, "&#95;", "_")

	return s
}

func main() {
	fmt.Println("开始使用Colly并发爬取阿德莱德大学员工信息...")

	var allStaff []StaffMember
	var mutex sync.Mutex
	var wg sync.WaitGroup

	// 创建Colly收集器
	c := colly.NewCollector(
		colly.UserAgent("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"),
	)

	// 设置请求延迟
	c.Limit(&colly.LimitRule{
		DomainGlob:  "*",
		Parallelism: 5, // 并发数
		Delay:       1 * time.Second,
	})

	// 设置回调函数
	c.OnHTML("table#bztable1 tbody tr", func(e *colly.HTMLElement) {
		// 跳过表头
		if e.DOM.Find("th").Length() > 0 {
			return
		}

		// 提取员工信息
		staff := extractStaffInfo(e)
		if staff.Name != "" {
			mutex.Lock()
			allStaff = append(allStaff, staff)
			mutex.Unlock()
		}
	})

	c.OnRequest(func(r *colly.Request) {
		fmt.Printf("正在访问: %s\n", r.URL.String())
	})

	c.OnError(func(r *colly.Response, err error) {
		fmt.Printf("访问 %s 时出错: %v\n", r.Request.URL, err)
	})

	// 并发爬取10页
	for page := 1; page <= 100; page++ {
		wg.Add(1)
		go func(pageNum int) {
			defer wg.Done()

			url := fmt.Sprintf("https://www.adelaide.edu.au/directory/atoz?m=atoz;dsn=directory.phonebook;orderby=last%%2Cfirst%%2Cposition_n;perpage=50;page=%d", pageNum)

			err := c.Visit(url)
			if err != nil {
				fmt.Printf("爬取第 %d 页时出错: %v\n", pageNum, err)
			}
		}(page)
	}

	// 等待所有协程完成
	wg.Wait()

	fmt.Printf("总共爬取到 %d 条员工信息\n", len(allStaff))

	// 保存为JSON文件
	if err := saveToJSON(allStaff); err != nil {
		fmt.Printf("保存JSON文件失败: %v\n", err)
	} else {
		fmt.Println("JSON文件保存成功")
	}

	// 保存为CSV文件
	if err := saveToCSV(allStaff); err != nil {
		fmt.Printf("保存CSV文件失败: %v\n", err)
	} else {
		fmt.Println("CSV文件保存成功")
	}
}

func extractStaffInfo(e *colly.HTMLElement) StaffMember {
	var staff StaffMember

	// 提取电话
	phoneText := e.ChildText("td[data-th='Telephone'] strong")
	if phoneText != "" {
		// 获取完整的电话号码（包括831前缀）
		fullPhoneText := e.ChildText("td[data-th='Telephone']")
		if strings.Contains(fullPhoneText, "831") {
			staff.Phone = "831 " + phoneText
		} else {
			staff.Phone = phoneText
		}
	}

	// 提取姓名链接和URL
	nameLinks := e.ChildAttrs("td[data-th='Family Name'] a, td[data-th='Given Name'] a", "href")
	if len(nameLinks) > 0 {
		staff.ProfileURL = "https://www.adelaide.edu.au" + nameLinks[0]
	}

	// 提取姓氏和名字
	familyName := strings.TrimSpace(e.ChildText("td[data-th='Family Name']"))
	givenName := strings.TrimSpace(e.ChildText("td[data-th='Given Name']"))

	if familyName != "" && givenName != "" {
		staff.Name = givenName + " " + familyName
	}

	// 提取职位
	staff.Title = strings.TrimSpace(e.ChildText("td[data-th='Position']"))

	// 提取邮箱
	emailLink := e.ChildAttr("td[data-th='Email'] a[href^='mailto:']", "href")
	if emailLink != "" {
		email := strings.TrimPrefix(emailLink, "mailto:")
		staff.Email = decodeHTMLEntities(email)
	}

	return staff
}

func saveToJSON(staff []StaffMember) error {
	file, err := os.Create("staff_data.json")
	if err != nil {
		return err
	}
	defer file.Close()

	encoder := json.NewEncoder(file)
	encoder.SetIndent("", "  ")
	return encoder.Encode(staff)
}

func saveToCSV(staff []StaffMember) error {
	file, err := os.Create("staff_data.csv")
	if err != nil {
		return err
	}
	defer file.Close()

	writer := csv.NewWriter(file)
	defer writer.Flush()

	// 写入CSV头部
	header := []string{"姓名", "职位", "邮箱", "电话", "个人资料URL"}
	if err := writer.Write(header); err != nil {
		return err
	}

	// 写入数据
	for _, member := range staff {
		record := []string{
			member.Name,
			member.Title,
			member.Email,
			member.Phone,
			member.ProfileURL,
		}
		if err := writer.Write(record); err != nil {
			return err
		}
	}

	return nil
}
